import cv2
import numpy as np
import os
import glob
from datetime import datetime
from ultralytics import YOLO
from face_recognizer import get_face_embedding, save_face_image, log_event
from db_logger import init_db, log_to_db, update_visitor_count

# Configs
EXIT_TIMEOUT = 5.0  # seconds before considering face exited
SIMILARITY_THRESHOLD = 0.7

# Init
model = YOLO("yolov8n.pt")
init_db()

# Mappings
known_faces = []
face_ids = []
last_seen = {}
exited = set()
id_counter = 1

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def assign_id():
    global id_counter
    id_val = f"ID-{id_counter:03d}"
    id_counter += 1
    return id_val

video_paths = glob.glob("videos/rec*.mp4")
if not video_paths:
    print("❌ No videos found in videos/rec*.mp4")
    exit()

for path in video_paths:
    print(f"\n🎥 Processing: {path}")
    cap = cv2.VideoCapture(path)

    frame_faces = {}  # ID to box map

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = datetime.now().timestamp()
        results = model.predict(frame, conf=0.5, save=False, verbose=False)
        current_ids = set()

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face_img = frame[y1:y2, x1:x2]
            if face_img.size == 0:
                continue

            embedding = get_face_embedding(face_img)
            if embedding is None:
                continue

            matched_id = None
            for idx, known in enumerate(known_faces):
                sim = cosine_similarity(embedding, known)
                if sim > SIMILARITY_THRESHOLD:
                    matched_id = face_ids[idx]
                    break

            if matched_id is None:
                matched_id = assign_id()
                known_faces.append(embedding)
                face_ids.append(matched_id)
                image_path = save_face_image(face_img, matched_id)
                log_event("ENTRY", matched_id, image_path)
                log_to_db(matched_id, image_path)
                print(f"[ENTRY] {matched_id}")

            current_ids.add(matched_id)
            last_seen[matched_id] = timestamp

            # Draw green box + ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{matched_id} (ENTRY)", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Check EXITs
        for face_id in list(last_seen.keys()):
            if face_id not in current_ids and face_id not in exited:
                if timestamp - last_seen[face_id] > EXIT_TIMEOUT:
                    log_event("EXIT", face_id)
                    exited.add(face_id)
                    print(f"[EXIT] {face_id}")

        cv2.imshow("Face Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

cv2.destroyAllWindows()

# Final count
unique_count = len(set(face_ids))
update_visitor_count(unique_count)
print(f"\n✅ Unique Visitors: {unique_count}")
