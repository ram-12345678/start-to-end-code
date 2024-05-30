from flask import Flask, Response, jsonify
import cv2
import threading

app = Flask(__name__)
camera = cv2.VideoCapture(0)
output_frame = None
lock = threading.Lock()
recording = False
recorded_frames = []

@app.route('/video_feed')
def video_feed():
    def generate():
        global output_frame, lock
        while True:
            with lock:
                if output_frame is None:
                    continue
                ret, encoded_image = cv2.imencode('.jpg', output_frame)
                if not ret:
                    continue
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording')
def start_recording():
    global recording
    recording = True
    return jsonify(status="Recording started")

@app.route('/stop_recording')
def stop_recording():
    global recording, recorded_frames
    recording = False
    save_recording()
    recorded_frames = []
    return jsonify(status="Recording stopped")

@app.route('/pause_recording')
def pause_recording():
    global recording
    recording = False
    return jsonify(status="Recording paused")

def save_recording():
    global recorded_frames
    if not recorded_frames:
        return
    height, width, layers = recorded_frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for frame in recorded_frames:
        out.write(frame)
    out.release()

def capture_frames():
    global output_frame, lock, recording, recorded_frames
    while True:
        ret, frame = camera.read()
        if not ret:
            continue
        with lock:
            output_frame = frame.copy()
        if recording:
            recorded_frames.append(frame)

if __name__ == '__main__':
    t = threading.Thread(target=capture_frames)
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
