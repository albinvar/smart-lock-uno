import cv2
import os
import numpy as np
import threading
import time
import src.shared as shared
import config

# global serial object.
ser = None

# Initialize Face Recognition Model
face_cascade = cv2.CascadeClassifier(config.face_recognition_model)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(config.face_recognition_trainer)
names = []

# Load Preprocessed Images and Assign Labels
for name in os.listdir(config.face_recognition_faces):
    names.append(name)

# Define the function for voice output
def voice_output(name, is_authorized=True):

    if is_authorized:
        # Speak the authorized message
        shared.voice_feedback_queue.put(f"{name} is authorized. Disengaging locks.")
    else:
        # Speak the unauthorized message
        shared.voice_feedback_queue.put(f"Unauthorized access detected")


# Define the function to recognize faces and save unauthorized faces
def recognize_face(ser):
    # Initialize Webcam
    cap = cv2.VideoCapture(config.video_capture_device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.video_capture_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.video_capture_height)

    # Initialize Variables to Track Unauthorized Access
    unauthorized_count = 0
    max_unauthorized_count = config.max_unauthorized_count
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
            if conf <= config.camera_threshold:
                name = names[id_]
                cv2.putText(img, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                # Add Your Code to Trigger Authentication Here
                if name != "Unauthorized":
                     if not authorized_detected:
                        authorized_detected = True
                        # Unlock the solenoid lock here

                        # Thread the voice output
                        # voice_thread = threading.Thread(target=voice_output, args=(name,))
                        # voice_thread.start()

                        # use main thread instread of voice_thread
                        voice_output(name)

                        # Unlock the solenoid lock for x seconds
                        ser.write(b'u')

                        notification_message = f"🚪 *Door unlocked*\n\n"\
                        f"*Unlock details*\n"\
                        f"User : {name}\n"\
                        f"Unlock method : facial authentication\n"\
                        f"Unlock duration : {config.camera_authroized_delay} sec \n"\
                        f"Unlock action : unlock"
                        if config.telegram_notifications:
                            shared.send_message(notification_message)

                        time.sleep(config.camera_authroized_delay)
                        ser.write(b'l')
                        
                        # Pause the camera for 10 seconds after an authorized face is detected
                        # time.sleep(10)
                        # authorized_detected = False
                        # As far as authroized_detected remains true. This block wont be executed. Means, just one time execution.
                        print(f"{name} has been authorized")

            else:
                cv2.putText(img, "Unauthorized", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                unauthorized_count += 1

                # Save unauthorized person image and reset unauthorized_count
                if unauthorized_count >= max_unauthorized_count:
                    folder_name = config.face_recognition_intruders_folder
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)
                    current_time = int(time.time())
                    file_name = os.path.join(folder_name, f"unauthorized_{current_time}.jpg")
                    cv2.imwrite(file_name, img)
                    print(f"intruder detected, image saved to {file_name}")
                    unauthorized_count = 0

                    voice_output(name, False)
                    
                    notification_message = f"🚪 *Intruder Detected*\n\n"\
                       f"*details*\n\n"\
                       f"Unlock method: facial recognition\n"\
                       f"Unlock action: unlock"
                    if config.telegram_notifications:
                            shared.send_message(notification_message)

        cv2.imshow('Facial Recognition', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
