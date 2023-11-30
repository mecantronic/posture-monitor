from flask import Flask
from flask import render_template
from flask import Response
from flask import request, redirect, url_for
import cv2
from posture_analyzer import process_frame
import os

# Initialize Flask object.
app = app = Flask(__name__, template_folder='templates')

def generate_frames(video_path=0):

    # For file input, replace file name with <path>.
    cap = cv2.VideoCapture(video_path) if video_path else cv2.VideoCapture(0)
    fps = cap.get(cv2.CAP_PROP_FPS) # Get fps.
    width = int(cap.get(3))
    height = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('video_output.mp4', fourcc, fps, (width, height))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Posture analyzer process (MediaPipe)
        result = process_frame(frame, fps)
        out.write(result)

        ret, buffer = cv2.imencode('.jpg', result)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    out.release()
     
@app.route("/")
def login():
     return render_template("login.html")

@app.route("/video_input")
def index():
     return render_template("video_input.html")

@app.route("/term_conditions")
def term_conditions():
     return render_template("term_conditions.html")

@app.route("/choose_activity")
def select_activity():
     return render_template("select_activity.html")

@app.route('/video_feed', methods=['POST'])
def video_feed():

    use_webcam = request.form.get('use_webcam')  # Obtener el valor del checkbox
    videoOptions = request.form.get('videoOptions')
    if use_webcam:
        video_path = 0  # Establecer el valor a '0' si el checkbox está seleccionado
    elif videoOptions  != 'Nothing':
        video_path = os.path.join('uploads', videoOptions + '.mp4')
    else:
        if 'file' not in request.files:
            return render_template('video_input.html', error='No file was selected')

        file = request.files['file']
        if file.filename == '':
            return render_template('video_input.html', error='No file was selected')
        
        video_path = os.path.join('uploads', 'video_input.mp4')
        file.save(video_path)
    return Response(generate_frames(video_path),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video_play")
def video_play():
     return render_template("video_play.html")

if __name__ == "__main__":
    app.run(debug=True)