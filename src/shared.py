import requests
import config
import queue
import threading
import pyttsx3
import time

ser = None


# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('rate', config.voice_rate)
engine.setProperty('voice', voices[config.voice].id)  # Change the index to select a different voice

# Initialize thread-safe queue for voice feedback messages
voice_feedback_queue = queue.Queue()

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

# Start thread for handling voice feedback
voice_thread = threading.Thread(target=handle_voice_feedback, daemon=True)
voice_thread.start()

def send_message(message):
    # Send a message to the Telegram bot
    url = f'https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage'
    data = {
        'chat_id': config.telegram_chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)