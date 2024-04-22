from flask import Flask, Response, session, render_template,request
import cv2
from YOLOWebcam import RunYOLOWebcam

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'seba'


class_name=""
last_classes=[]
@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    print(request.form)
    global video_name
    video_name = request.form.get('video_name').split('.')[0]
    print(f'Video: {video_name}')
    return video_name

def generate_frames(path_x):
    global class_name  # Declare class_name as global to modify it within this function
    yolo_output = RunYOLOWebcam(path_x)  
    for detection_, classes in yolo_output:
        if len(classes) > 0: 
            global last_classes
            last_classes=classes
        if video_name != "" and class_name == video_name:
                print(f'Video: {video_name}' , f'Class: {class_name}')
                print("Detected class matches current video name. Stopping detection.")
                last_classes=class_name
                break  # Exit the loop to stop the detection
        #print(last_classes)
        ref,buffer=cv2.imencode('.jpg',detection_)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n') 
      # Reset class_name after iteration is done

@app.route('/get_class')
def get_class():
    #global class_name
    global last_classes
    if len(last_classes) > 0: 
        val = last_classes[-1]
        last_classes=[]
        print(last_classes)
        return val
    return last_classes


    

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