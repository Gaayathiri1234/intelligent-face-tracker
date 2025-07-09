Intelligent Face Tracker

This project automatically:
- Detects faces from videos
- Assigns a permanent ID to each face (e.g., ID‑001)
- Tracks when a person enters and exits the frame
- Saves a photo when they enter
- Keeps a log of entry and exit times
- Records everything in a database and CSV files

---

 Tech Used
- Python 
- YOLOv8 (face detection)
- InsightFace (face recognition)
- OpenCV (video and drawing)
- SQLite (database)
- CSV export

---

Where Files Are
intelligent_face_tracker/
│
├── detector.py # Main program
├── face_recognizer.py # Detect and save faces
├── db_logger.py # Save logs to database
├── export_to_csv.py # Make CSV reports
├── requirements.txt # Required Python packages
├── videos/ # Put your video files here
├── logs/ # Saved face images and events.log
├── exports/ # CSV files are saved here
└── README.md # This file


---

 How to Run

1. Open terminal in project folder  
2. Create a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3. Install packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Add your videos into `videos/` folder  
5. Run main program:
    ```bash
    python detector.py
    ```

---

What You’ll See

- Green boxes with IDs show on video window  
- When someone enters, a face photo saves in `logs/entries/DATE/`  
- An `events.log` entry is created  
- When they exit, the exit time is logged  
- CSV reports are generated in `exports/` after running `export_to_csv.py`



# intelligent-face-tracker
Hackathon Project: AI-based Visitor Detection with Auto Face Tracking
