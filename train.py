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