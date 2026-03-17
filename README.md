# Modern Detection Dashboard

This adds a lightweight Flask dashboard that streams webcam frames processed by YOLOv8 and shows live counts for dogs and cell phones.

Files added:

- `dashboard.py` — Flask app that runs the capture thread and serves the MJPEG stream and counts.
- `templates/index.html` — Dashboard UI using Bootstrap.
- `static/css/styles.css` — Minimal styling.
- `requirements.txt` — Python dependencies.

Quick start (Windows PowerShell):

```powershell
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python dashboard.py
```

Open http://localhost:5000 in your browser. Press Ctrl+C to stop.

Notes:
- The app uses `yolov8n.pt` in the workspace by default. Replace the model path in `dashboard.py` to use a different weights file.
- If your camera is busy, close other apps using the webcam.
