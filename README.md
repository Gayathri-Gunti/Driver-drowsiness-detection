**Driver Drowsiness Detection 🚗💤**

This project detects driver drowsiness in real time using OpenCV and MediaPipe FaceMesh.
If the driver’s eyes remain closed beyond a safe limit, an alarm is triggered automatically to alert the driver. Once the driver opens their eyes, the alarm stops automatically.

**🔹 Features**

Real-time eye tracking using MediaPipe Face Mesh

Calculates Eye Aspect Ratio (EAR) to determine if eyes are closed

Triggers an alarm sound when drowsiness is detected

Automatically stops alarm when eyes open

Uses rolling buffer to filter out normal blinks (prevents false alarms)

**🔹 Workflow (How it works)**

Capture Webcam Feed – OpenCV captures live video from the laptop’s webcam.

Face Landmark Detection – MediaPipe detects facial landmarks including eyes.

EAR Calculation – Eye Aspect Ratio (EAR) is computed using eye landmarks.

If EAR < threshold → eyes considered closed

If EAR ≥ threshold → eyes open

Blink Filtering – A short blink won’t trigger alarm. Only prolonged closure triggers alarm.

**Alarm System –**

If eyes are closed for ~1 second → Alarm rings

When eyes open → Alarm stops automatically

Live Display – The frame shows webcam feed and warning message "WAKE UP!" when drowsiness is detected.

**output:**
if the user is in awake
<img width="1670" height="979" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/d7a52e1e-4138-449c-8cb1-c155ee9d29ac" />


if the user is in drowsy

<img width="1661" height="966" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/187bf40e-cbcf-4bea-a304-7e6711df719d" />

