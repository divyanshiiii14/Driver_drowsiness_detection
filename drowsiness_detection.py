import cv2
import dlib
import serial
import time
import numpy as np
import platform
from scipy.spatial import distance as dist

# =====================
# SOUND ALERT (BEEP)
# =====================
if platform.system() == "Windows":
    import winsound
    def play_beep():
        winsound.Beep(1000, 500)  # 1000 Hz, 0.5 sec
else:
    import os
    def play_beep():
        os.system('play -nq -t alsa synth 0.5 sine 1000 > /dev/null 2>&1')

# =====================
# SERIAL COMMUNICATION
# =====================
try:
    esp = serial.Serial('COM6', 115200, timeout=1)  # Change COM port if needed
    time.sleep(2)
    print("✅ ESP32 connected successfully.")
except:
    esp = None
    print("⚠️ ESP32 not connected. Running in camera-only mode.")

# =====================
# DLIB FACE + EYE DETECTOR
# =====================
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# =====================
# FUNCTIONS
# =====================
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def get_head_tilt_angle(landmarks):
    left_eye = landmarks[36]
    right_eye = landmarks[45]
    nose_tip = landmarks[33]
    eye_line = np.arctan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])
    angle_deg = np.degrees(eye_line)
    nose_y = nose_tip[1]
    return angle_deg, nose_y

# =====================
# CONSTANTS
# =====================
EYE_AR_THRESH = 0.22
EYE_AR_CONSEC_FRAMES = 15
TILT_ANGLE_THRESH = 15
NOSE_Y_DOWN_THRESH = 15
NO_FACE_LIMIT = 20

COUNTER = 0
ALARM_ON = False
NO_FACE_FRAMES = 0

# =====================
# VIDEO CAPTURE
# =====================
cap = cv2.VideoCapture(0)  # Change to your ESP32 stream URL if using camera module

while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Failed to grab frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray, 0)

    if len(faces) == 0:
        NO_FACE_FRAMES += 1
        if NO_FACE_FRAMES > NO_FACE_LIMIT:
            ALARM_ON = True
            status = "NO FACE DETECTED"
            play_beep()
            if esp:
                esp.write(b'1')
        else:
            status = "SEARCHING FACE..."
        cv2.putText(frame, f"Status: {status}", (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    else:
        NO_FACE_FRAMES = 0
        for face in faces:
            shape = predictor(gray, face)
            shape = np.array([[p.x, p.y] for p in shape.parts()])

            leftEye = shape[36:42]
            rightEye = shape[42:48]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            angle_deg, nose_y = get_head_tilt_angle(shape)

            for (x, y) in np.concatenate((leftEye, rightEye), axis=0):
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            if ear < EYE_AR_THRESH:
                COUNTER += 1
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    ALARM_ON = True
                    status = "DROWSY"
                    play_beep()
            else:
                COUNTER = 0
                ALARM_ON = False
                status = "AWAKE"

            if abs(angle_deg) > TILT_ANGLE_THRESH or nose_y > face.bottom() - NOSE_Y_DOWN_THRESH:
                ALARM_ON = True
                status = "HEAD TILTED"
                play_beep()

            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Tilt: {angle_deg:.1f}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Status: {status}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255) if ALARM_ON else (0, 255, 0), 2)

            if esp:
                esp.write(b'1' if ALARM_ON else b'0')

    cv2.imshow("Drowsiness, Head Tilt & Face Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if esp:
    esp.close()
