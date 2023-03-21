import threading
import time
import signal
import sys

# Import the modules for each authentication method
from facial import recognize_face
# from rfid import read_rfid
from website import app

# Start the threads for each authentication method
face_thread = threading.Thread(target=recognize_face)
# rfid_thread = threading.Thread(target=read_rfid)
web_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})

face_thread.daemon = True
# rfid_thread.daemon = True
web_thread.daemon = True

face_thread.start()
# rfid_thread.start()
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
