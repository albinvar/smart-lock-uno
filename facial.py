import cv2
import os
import numpy as np

# Initialize Face Recognition Model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
names = []

# Load Preprocessed Images and Assign Labels
def load_images(path):
    images = []
    labels = []
    for name in os.listdir(path):
        label = len(names)
        names.append(name)
        dir_path = os.path.join(path, name)
        for filename in os.listdir(dir_path):
            img_path = os.path.join(dir_path, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
                labels.append(label)
    return images, np.array(labels)

images, labels = load_images('faces')

# Train Face Recognition Model
recognizer.train(images, labels)
recognizer.save('trainer.yml')

# Initialize Webcam
cap = cv2.VideoCapture(4)

# Recognize Faces in Real Time
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)
        if conf <= 70:
            name = names[id_]
            cv2.putText(img, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Add Your Code to Trigger Authentication Here
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow('Facial Recognition', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
