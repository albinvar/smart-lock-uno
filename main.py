import threading
import time
import signal
import sys
import serial
import src.shared as shared
import config

# Import the modules for each authentication method
from src.facial import recognize_face
from src.rfid import rfid_processor
from src.website import app

# Create a shared serial object
# try to open the serial port
try:
    shared.ser = serial.Serial(config.serial_port, config.serial_baud)
except serial.SerialException:
    # if it fails, exit the program
    print("Could not open serial port. Is the Arduino connected?")
    print("Please check the serial port and baud rate in config.py")
    print("Exiting...")
    sys.exit(1)

# Start the threads for each authentication method

if 'face' in config.auth_methods:
    face_thread = threading.Thread(target=recognize_face, args=(shared.ser,))
    face_thread.daemon = True
    face_thread.start()
if 'card' in config.auth_methods:
    rfid_thread = threading.Thread(target=rfid_processor, args=(shared.ser, config.authorized_cards))
    rfid_thread.daemon = True
    rfid_thread.start()
if 'api' in config.auth_methods:
    web_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    web_thread.daemon = True
    web_thread.start()

def signal_handler(signal, frame):
    print("\nStopping all threads...")
    for t in threading.enumerate():
        if t != threading.current_thread():
            t._stop()
    sys.exit(0)

# Register the signal handler for SIGINT
signal.signal(signal.SIGINT, signal_handler)

# Main loop
while True:
    # Add your code here to control the solenoid lock based on authentication
    time.sleep(1)
