import cv2
import os
import numpy as np
import threading
import time



# Initialize Face Recognition Model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
names = []

# Load Preprocessed Images and Assign Labels
for name in os.listdir('faces'):
    names.append(name)

# Define the function to recognize faces
def recognize_face():
    # Initialize Webcam
    cap = cv2.VideoCapture(4)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 990)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)

    # Recognize Faces in Real Time
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            if conf <= 250:
                name = names[id_]
                cv2.putText(img, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Add Your Code to Trigger Authentication Here
            else:
                cv2.putText(img, "Unauthorized", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow('Facial Recognition', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()