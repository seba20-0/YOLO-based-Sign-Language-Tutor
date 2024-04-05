from flask import Flask, Response, session, render_template
import cv2
from YOLOWebcam import RunYOLOWebcam

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'seba'

def generate_frames(path_x):
    yolo_output = RunYOLOWebcam(path_x)  
    for detection_ in yolo_output:
        ret, buffer = cv2.imencode('.jpg', detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('index.html')

@app.route('/lesson', methods=['GET', 'POST'])
def lesson():
    session.clear()
    return render_template('lesson.html')

@app.route('/video_stream')
def video_stream():
    return Response(generate_frames(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    app.run(debug=True)