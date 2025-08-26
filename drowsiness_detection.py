import cv2
import mediapipe as mp
import numpy as np
import threading
import pygame
import time

# -------------------------------
# Alarm setup
# -------------------------------
alarm_on = False
pygame.mixer.init()

def play_alarm():
    while alarm_on:
        pygame.mixer.music.load("alarm.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

# -------------------------------
# MediaPipe Face Mesh
# -------------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5
)

# Eye landmarks
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# -------------------------------
# EAR calculation
# -------------------------------
def eye_aspect_ratio(landmarks, eye_points, w, h):
    coords = [(int(landmarks[p].x * w), int(landmarks[p].y * h)) for p in eye_points]
    A = np.linalg.norm(np.array(coords[1]) - np.array(coords[5]))
    B = np.linalg.norm(np.array(coords[2]) - np.array(coords[4]))
    C = np.linalg.norm(np.array(coords[0]) - np.array(coords[3]))
    ear = (A + B) / (2.0 * C)
    return ear

# -------------------------------
# Parameters
# -------------------------------
EAR_THRESHOLD = 0.22       # Eyes below this considered closed
FRAME_BUFFER = 10          # Rolling buffer frames
EYE_CLOSED_FRAMES = 20     # Consecutive frames to trigger alarm (~1 sec)
frame_buffer = []
frame_counter = 0

# -------------------------------
# Start webcam
# -------------------------------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    avg_ear = 1.0  # default: eyes open
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
        avg_ear = (left_ear + right_ear) / 2.0

    # -------------------------------
    # Smooth EAR
    # -------------------------------
    frame_buffer.append(avg_ear)
    if len(frame_buffer) > FRAME_BUFFER:
        frame_buffer.pop(0)

    smooth_ear = np.mean(frame_buffer)

    # -------------------------------
    # Blink filtering
    # -------------------------------
    # Only consider eyes closed if smooth_ear stays below threshold for EYE_CLOSED_FRAMES
    if smooth_ear < EAR_THRESHOLD:
        frame_counter += 1
        if frame_counter >= EYE_CLOSED_FRAMES and not alarm_on:
            alarm_on = True
            t = threading.Thread(target=play_alarm)
            t.daemon = True
            t.start()
            print("Drowsiness detected! Alarm ON!")
    else:
        frame_counter = 0
        alarm_on = False

    # -------------------------------
    # Display alert
    # -------------------------------
    if alarm_on:
        cv2.putText(frame, "WAKE UP!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
