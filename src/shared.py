import requests
import config

ser = None

def send_message(message):
    # Send a message to the Telegram bot
    url = f'https://api.telegram.org/bot{config.telegram_bot_token}/sendMessage'
    data = {
        'chat_id': config.telegram_chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)