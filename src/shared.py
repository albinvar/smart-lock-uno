import requests
import config
import queue
import threading
import pyttsx3
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ser = None


# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('rate', config.voice_rate)
engine.setProperty('voice', voices[config.voice].id)  # Change the index to select a different voice

# Initialize thread-safe queue for voice feedback messages
voice_feedback_queue = queue.Queue()

# Initialize threa-safe queue for sending auth logs to server
logger_queue = queue.Queue()

# Define function to handle voice feedback
def handle_voice_feedback():
    while True:
        if not voice_feedback_queue.empty():
            message = voice_feedback_queue.get()
            engine.say(message)
            engine.startLoop(False)
            engine.iterate()
            engine.endLoop()
        time.sleep(0.1)


# Define function to handle sending auth logs to server
def handle_logger():
    while True:
        if not logger_queue.empty():
            log = logger_queue.get()
            send_auth_log_to_server(log['status'], log['type'], log['message'])
        time.sleep(0.1)

# Start thread for handling voice feedback
voice_thread = threading.Thread(target=handle_voice_feedback, daemon=True)
voice_thread.start()

# Start thread for handling sending auth logs to server
logger_thread = threading.Thread(target=handle_logger, daemon=True)
logger_thread.start()

def send_message(message):
    # Send a message to the Telegram bot
    url = f'https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage'
    data = {
        'chat_id': config.telegram_chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)

def send_photo(photo_path):
    # Send a photo to the Telegram bot
    url = f'https://api.telegram.org/bot{config.telegram_bot_token}/sendPhoto'
    data = {
        'chat_id': config.telegram_chat_id,
    }
    files = {
        'photo': open(photo_path, 'rb')
    }
    requests.post(url, data=data, files=files)

def send_auth_log_to_server(status, type, message):
    if config.auth_logging_enabled == False:
        return
    api_url = config.log_server_endpoint

    data = {
        'status': status,  # 'success' or 'failure
        'type': type,
        'message': message
    }

    try:
        response = requests.post(api_url, json=data)

        if response.status_code == 201:  # 201 indicates successful creation
            print("Auth log sent successfully")
        else:
            print(f"Failed to send auth log: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def greeting():
    current_time = time.localtime().tm_hour
    
    if 5 <= current_time < 12:
        return "Good morning"
    elif 12 <= current_time < 17:
        return "Good afternoon"
    elif 17 <= current_time < 20:
        return "Good evening"
    else:
        return "I hope you had a great day "