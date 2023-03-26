# Configuration File


# set video capture device
video_capture_device = 2

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

# Set the path to the face recognition model.
# This is the model that is used to detect faces.
face_recognition_model = 'haarcascade_frontalface_default.xml'

# Set the path to the face recognition trainer.
# This is the model that is used to recognize faces.
face_recognition_trainer = 'trainer.yml'

# Set the path to the face recognition faces.
# This is the folder that contains the faces to be recognized.
face_recognition_faces = 'faces'


# set video capture width
video_capture_width = 990

# set video capture height
video_capture_height = 540