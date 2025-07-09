import cv2
import os
from datetime import datetime
from insightface.app import FaceAnalysis

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

def get_face_embedding(img):
    faces = app.get(img)
    if faces:
        return faces[0].embedding
    return None

def save_face_image(face_img, face_id):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("logs", "entries", today)
    os.makedirs(folder, exist_ok=True)
    filename = f"{face_id}_{datetime.now().strftime('%H%M%S')}.jpg"
    path = os.path.join(folder, filename)
    cv2.imwrite(path, face_img)
    return path

def log_event(event_type, face_id, img_path="", log_file="logs/events.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{event_type}] {face_id} at {timestamp}"
    if img_path:
        line += f" | {img_path}"
    line += "\n"
    with open(log_file, "a") as f:
        f.write(line)
