# Configuration File

# set all available authentification methods
auth_methods = ['card', 'face', 'api']

# enable telegram notifications
telegram_notifications = True

# telegram bot token
telegram_bot_token = '123456789:ABCDEF1234567890ABCDEF1234567890ABC'
telegram_chat_id = '123456789'

# set video capture device
video_capture_device = 1

# Set threshold for camera to detect face.
# Lower threshold means more sensitive, but more false positives.
camera_threshold = 85

# Set the time to wait before checking for a new face.
# This is to prevent the camera from constantly checking for a new face.
camera_authroized_delay = 7

# set the serial port
serial_port = 'COM3'

# set the serial baud rate
serial_baud = 9600

# Array of authorized card IDs
authorized_cards = []

# rfid authorized delay
rfid_authorized_delay = 5

# Voice synthesis engine
# set the voice
voice = 1

# Set the voice rate
voice_rate = 140

# web api password
web_api_password = '1234'

# Set the path to the face recognition model.
# This is the model that is used to detect faces.
face_recognition_model = 'haarcascade_frontalface_default.xml'

# Set the path to the face recognition trainer.
# This is the model that is used to recognize faces.
face_recognition_trainer = 'trainer.yml'

face_recognition_intruders_folder = 'intruders'

# Set the path to the face recognition faces.
# This is the folder that contains the faces to be recognized.
face_recognition_faces = 'faces'


# set video capture width
video_capture_width = 990

# set video capture height
video_capture_height = 540


# max unauthorized count for facial recognition
max_unauthorized_count = 100


# telegram notification api
telegram_notification_api = ''