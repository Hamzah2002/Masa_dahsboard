from flask import Flask, Response
import cv2
import atexit
import threading

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Open the default camera

def release_camera():
    """Release the camera resource when the script exits or an error occurs."""
    if camera.isOpened():
        camera.release()
        print("Camera released.")

# Register the release function to be called on exit
atexit.register(release_camera)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Stream video frames to the client."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def run_video_stream():
    """Run the Flask app for video streaming."""
    try:
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except OSError as e:
        print(f"Socket Error: {e}")
        release_camera()
