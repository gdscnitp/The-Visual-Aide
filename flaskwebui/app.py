from asyncio.windows_events import NULL
from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)
camera=NULL
flag=True
def generate_frames(camera):
        global flag
        while flag:
            
            ##Camera frames
            success,frame=camera.read()
            if not success:
                break
            else:
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()

            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    
        
# def camera_off():
#     flag=False
#     # camera.release()
        
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    # flag=True
    global camera
    camera = cv2.VideoCapture(0)
    return Response(generate_frames(camera),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/videoff')
def videoff():
    global flag
    flag=False
    global camera
    camera.release()
    return render_template('index.html')

@app.route('/videon')
def videon():
    global flag
    flag=True
    return render_template('index.html')


if __name__=="__main__":
    app.run(debug=True)