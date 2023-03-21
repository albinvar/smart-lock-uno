import cv2
import os
import numpy as np
import threading
import time
import pyttsx3
import requests


# Initialize Face Recognition Model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
names = []

# Load Preprocessed Images and Assign Labels
for name in os.listdir('faces'):
    names.append(name)

# Define the function for voice output
def voice_output(name, is_authorized=True):

    # Initialize Voice Output
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    newVoiceRate = 140
    engine.setProperty('rate', newVoiceRate)
    engine.setProperty('voice', voices[1].id)  # Change the index to select a different voice

    if is_authorized:
        # Speak the authorized message
        engine.say(f"{name} is authorized. Disengaging locks.")
    else:
        # Speak the unauthorized message
        notification_message = f"🚪 *Intruder Detected*\n\n"\
                       f"*details*\n\n"\
                       f"Unlock method: facial recognition\n"\
                       f"Unlock action: unlock"

        requests.post('https://lock-notification-api.lov3.pw', data={'message': notification_message})
        engine.say(f"Unauthorized access detected")
    engine.runAndWait()

    if engine._inLoop:
        engine.endLoop()

    # Clean up the engine
    engine.stop()


# Define the function to recognize faces and save unauthorized faces
def recognize_face():
    # Initialize Webcam
    cap = cv2.VideoCapture(4)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 990)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    # Initialize Variables to Track Unauthorized Access
    unauthorized_count = 0
    max_unauthorized_count = 100
    authorized_detected = False

    # Recognize Faces in Real Time
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        name = "Unauthorized"  # Default 'name' variable to Unauthorized
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            if conf <= 100:
                name = names[id_]
                cv2.putText(img, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                # Add Your Code to Trigger Authentication Here
                if name != "Unauthorized":
                     if not authorized_detected:
                        authorized_detected = True
                        # Unlock the solenoid lock here
                        voice_thread = threading.Thread(target=voice_output, args=(name,))
                        voice_thread.start()
                        # Pause the camera for 10 seconds after an authorized face is detected
                        # time.sleep(10)
                        # authorized_detected = False
                        # As far as authroized_detected remains true. This block wont be executed. Means, just one time execution.

            else:
                cv2.putText(img, "Unauthorized", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                unauthorized_count += 1

                # Save unauthorized person image and reset unauthorized_count
                if unauthorized_count >= max_unauthorized_count:
                    folder_name = 'intruders'
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    current_time = int(time.time())
                    file_name = os.path.join(folder_name, f"unauthorized_{current_time}.jpg")
                    cv2.imwrite(file_name, img)
                    unauthorized_count = 0
                    voice_thread = threading.Thread(target=voice_output, args=(name, False))
                    voice_thread.start()

        cv2.imshow('Facial Recognition', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
