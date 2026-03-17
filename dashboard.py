from flask import Flask, render_template, Response, jsonify
import threading
import time
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Load model (uses existing yolov8n.pt in workspace)
model = YOLO('yolov8n.pt')

lock = threading.Lock()
output_frame = None
counts = {"dog": 0, "phone": 0}


def capture_loop():
    global output_frame, counts
    # Try using DirectShow on Windows which often fixes camera access issues
    backends = [cv2.CAP_DSHOW, 0]
    cap = None
    for backend in backends:
        try:
            if backend == 0:
                c = cv2.VideoCapture(0)
            else:
                c = cv2.VideoCapture(0, backend)
            if c is not None and c.isOpened():
                cap = c
                break
            else:
                if c is not None:
                    c.release()
        except Exception:
            pass

    if cap is None or not cap.isOpened():
        print('Warning: camera not available. Video feed will show a placeholder.')
        # create a simple placeholder image
        placeholder = np.full((480, 640, 3), 240, dtype=np.uint8)
        cv2.putText(placeholder, 'No camera available', (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)
        ret2, jpeg = cv2.imencode('.jpg', placeholder)
        if ret2:
            with lock:
                output_frame = jpeg.tobytes()
        return
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            time.sleep(0.05)
            continue
        try:
            r = model(frame)[0]
            dog_count = sum(1 for b in r.boxes if int(b.cls[0]) == 16 and float(b.conf[0]) > 0.7)
            phone_count = sum(1 for b in r.boxes if int(b.cls[0]) == 67 and float(b.conf[0]) > 0.7)
            frame = r.plot()
        except Exception as e:
            # If model inference fails, keep showing raw frame and log error
            print('Model inference error:', e)
            dog_count = 0
            phone_count = 0

        with lock:
            counts["dog"] = int(dog_count)
            counts["phone"] = int(phone_count)
            ret2, jpeg = cv2.imencode('.jpg', frame)
            if ret2:
                output_frame = jpeg.tobytes()

    cap.release()


@app.route('/')
def index():
    return render_template('index.html')


def generate_mjpeg():
    global output_frame
    while True:
        with lock:
            frame = output_frame
        if frame is None:
            time.sleep(0.1)
            continue
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_mjpeg(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/counts')
def get_counts():
    with lock:
        return jsonify(counts)


if __name__ == '__main__':
    t = threading.Thread(target=capture_loop, daemon=True)
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
