from flask import Flask
from flask import render_template
from flask import Response
from flask import request, redirect, url_for
from posture_analyzer import process_frame_video
import os

# Initialize Flask object.
app = app = Flask(__name__, template_folder='templates')

def generate_output(video_path=0):

    if video_path == 0:
        pass
    else: 
        process_frame_video(video_path)
    
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

@app.route('/webcam')
def webcam_streaming():
     return render_template("webcam_streaming.html")

@app.route('/video_feed', methods=['POST'])
def video_feed():
    use_webcam = request.form.get('use_webcam')  # Obtener el valor del checkbox
    videoOptions = request.form.get('videoOptions')
    if use_webcam:
        video_path = 0  # Establecer el valor a '0' si el checkbox está seleccionado
    elif videoOptions  != 'Nothing':
        video_path = url_for('static', filename='assets/test-videos/Test_1.mp4')
        #video_path = os.path.join('../processing/downloads/', videoOptions + '.mp4')
        return render_template("video_feed.html", video_path=video_path)
    else:
        if 'file' not in request.files:
            return render_template('video_input.html', error='No file was selected')

        file = request.files['file']
        if file.filename == '':
            return render_template('video_input.html', error='No file was selected')
        
        video_path = os.path.join('processing/uploads', 'video_input.mp4')
        file.save(video_path)
        process_frame_video(video_path)

    #process_frame_video(video_path)
    #return Response(generate_frames(video_path),
    #               mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template("video_feed.html")

if __name__ == "__main__":
    app.run(debug=True)