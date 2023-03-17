import threading
import serial
import time
import cv2
import numpy as np
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from flask import Flask, render_template, request, redirect, url_for

# Initialize RFID Reader
reader = SimpleMFRC522()

# Initialize Arduino Serial Port
ser = serial.Serial('/dev/ttyACM0', 9600)

# Initialize GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# Initialize Face Recognition Model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')
names = ['Name1', 'Name2', 'Name3']

# Initialize Flags
face_detected = False
rfid_detected = False

# Function to Recognize Face
def recognize_face():
    global face_detected
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            if conf <= 70:
                name = names[id_ - 1]
                cv2.putText(img, name, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face_detected = True
            else:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.imshow('Face Recognition', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

# Function to Read RFID Tag
def read_rfid():
    global rfid_detected
    while True:
        id, text = reader.read()
        print(id)
        print(text)
        rfid_detected = True

# Start Threads
face_thread = threading.Thread(target=recognize_face)
rfid_thread = threading.Thread(target=read_rfid)
face_thread.start()
rfid_thread.start()

# Initialize Flask App
app = Flask(__name__)

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'mypassword':
            error = 'Invalid Password'
        else:
            return redirect(url_for('open_lock'))
    return render_template('login.html', error=error)

# Open Lock Page
@app.route('/open_lock')
def open_lock():
    if face_detected and rfid_detected:
        ser.write(bytes(1))
        GPIO.output(18, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(18, GPIO.LOW)
        face_detected = False
        rfid_detected = False
        return render_template('open_lock.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
