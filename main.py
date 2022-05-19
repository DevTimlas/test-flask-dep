from flask import Flask, render_template, Response
import cv2
import time
import mediapipe as mp




VISUALIZE_FACE_POINTS = False

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
drawing_spec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

nose_landmarks = [49, 279, 197, 2, 5]
app = Flask('hello')
camera = cv2.VideoCapture(0)
def gen_frames():  
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            results = faceMesh.process(rgb)
            
            if results.multi_face_landmarks:
            	for face_landmarks in results.multi_face_landmarks:
            		mpDraw.draw_landmarks(frame, face_landmarks, mpFaceMesh.FACEMESH_CONTOURS, drawing_spec)
            		for lm_id, lm in enumerate(face_landmarks.landmark):
            			h, w, c = rgb.shape
            			x, y = int(lm.x * w), int(lm.y * h)
            			
            			if lm_id in nose_landmarks:
            				cv2.putText(frame, str(lm_id), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 0, 255), 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/')
def index():
    return """<body>
<div class="container">
    <div class="row">
        <div class="col-lg-8  offset-lg-2">
            <h3 class="mt-5">Live Streaming</h3>
            <img src="/video_feed" width="50%">
        </div>
    </div>
</div>
</body>"""
app.run()
