import threading
import time

# Import the modules for each authentication method
from facial import recognize_face
# from rfid import read_rfid
from website import app

# Start the threads for each authentication method
face_thread = threading.Thread(target=recognize_face)
# rfid_thread = threading.Thread(target=read_rfid)
web_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})

face_thread.start()
# rfid_thread.start()
web_thread.start()

# Main loop
while True:
    # Add your code here to control the solenoid lock based on authentication
    time.sleep(1)




# import threading
# import time
# from website import app
# from facial import recognize_face

# # Define shared variable
# door_locked = False


# # Start the threads for each authentication method
# web_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
# face_thread = threading.Thread(target=recognize_face)

# face_thread.start()
# web_thread.start()

# # Main loop
# while True:
#     if door_locked:
#         # code to lock solenoid
#         message = "Locking the door now."
#     else:
#         # code to unlock solenoid
#         message = "Unlocking the door now."
#     # code for voice output message
#     print(message)
#     time.sleep(1)