import threading
import time
import signal
import sys
import serial
import shared
import config

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

# Import the modules for each authentication method
from facial import recognize_face
from rfid import rfid_processor
from website import app

# Start the threads for each authentication method
face_thread = threading.Thread(target=recognize_face, args=(shared.ser,))
rfid_thread = threading.Thread(target=rfid_processor, args=(shared.ser, config.authorized_cards))
web_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})

face_thread.daemon = True
rfid_thread.daemon = True
web_thread.daemon = True

face_thread.start()
rfid_thread.start()
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
