import cv2
import mediapipe as mp
import numpy as np
import os
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Open Webcam
cap = cv2.VideoCapture(0)  # Change index if using an external camera

# Speak function using espeak
def speak(text):
    print(f" Speaking: {text}")  # Debugging print
    os.system(f'espeak "{text}"')  # Linux speech synthesis

# Improved ASL Letter Recognition
def recognize_asl_letter(landmarks):
    thumb_tip = landmarks[4]  
    index_tip = landmarks[8]  
    middle_tip = landmarks[12]  
    ring_tip = landmarks[16]  
    pinky_tip = landmarks[20]  

    thumb_ip = landmarks[3]  # Thumb joint near palm
    index_mcp = landmarks[5]  # Index finger base
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    # ======== ASL "A" Detection ========
    is_fist = (index_tip[1] > index_mcp[1] and
               middle_tip[1] > middle_mcp[1] and
               ring_tip[1] > ring_mcp[1] and
               pinky_tip[1] > pinky_mcp[1])  # All fingers curled down

    thumb_positioned = thumb_tip[0] > index_mcp[0]  # Thumb on side

    if is_fist and thumb_positioned:
        return "A"

    # ======== ASL "B" Detection ========
    fingers_extended = (index_tip[1] < index_mcp[1] and
                        middle_tip[1] < middle_mcp[1] and
                        ring_tip[1] < ring_mcp[1] and
                        pinky_tip[1] < pinky_mcp[1])  # All fingers extended
    thumb_inside = thumb_tip[1] > index_mcp[1]  # Thumb is folded

    if fingers_extended and thumb_inside:
        return "B"

    # ======== ASL "C" Detection (Curved hand forming 'C') ========
    if (thumb_tip[0] > index_tip[0] and 
        pinky_tip[0] < ring_tip[0] and 
        abs(index_tip[1] - pinky_tip[1]) < 0.1):  
        return "C"

    # ======== ASL "O" Detection (Fingertips form a circle) ========
    if (abs(index_tip[0] - thumb_tip[0]) < 0.05 and 
        abs(middle_tip[0] - thumb_tip[0]) < 0.05 and
        abs(ring_tip[0] - thumb_tip[0]) < 0.05 and 
        abs(pinky_tip[0] - thumb_tip[0]) < 0.05):
        return "O"

    # ======== ASL "L" Detection ========
    is_index_up = index_tip[1] < middle_tip[1] and index_tip[1] < ring_tip[1] and index_tip[1] < pinky_tip[1]
    is_thumb_out = thumb_tip[0] < index_tip[0]  # Thumb sideways
    is_other_fingers_folded = (middle_tip[1] > index_tip[1] and
                               ring_tip[1] > index_tip[1] and
                               pinky_tip[1] > index_tip[1])

    if is_index_up and is_thumb_out and is_other_fingers_folded:
        return "L"

    # ======== ASL "V" Detection (Index & Middle finger extended, like Victory sign) ========
    if (index_tip[1] < middle_tip[1] and
        middle_tip[1] < ring_tip[1] and
        ring_tip[1] > index_tip[1] and 
        pinky_tip[1] > index_tip[1]):
        return "V"

    # ======== ASL "Y" Detection (Thumb & Pinky extended, like "Y") ========
    is_y = (thumb_tip[1] < index_tip[1] and 
            pinky_tip[1] < ring_tip[1] and 
            index_tip[1] > middle_tip[1] and 
            middle_tip[1] > ring_tip[1])
    
    if is_y:
        return "Y"

    return None

# Letter-to-Speech Mapping
letter_to_speech = {
    "A": "I need water",
    "B": "I need food",
    "C": "Please call for help",
    "O": "Okay, understood",
    "L": "I need help",
    "V": "I am feeling great",
    "Y": "Yes, I agree"
}

last_spoken = None
last_speak_time = time.time()

# Main Loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip image for mirror view
    frame = cv2.flip(frame, 1)

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)  # Detect hands

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmarks as (x, y) coordinates
            landmarks = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark])

            # Recognize ASL letter
            detected_letter = recognize_asl_letter(landmarks)

            if detected_letter:
                cv2.putText(frame, f"Detected: {detected_letter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Speak (only if not repeated in last 3 sec)
                current_time = time.time()
                if detected_letter != last_spoken or (current_time - last_speak_time) > 3:
                    speak(letter_to_speech[detected_letter])
                    last_spoken = detected_letter
                    last_speak_time = current_time

    # Show webcam feed
    cv2.imshow("ASL to Speech", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
