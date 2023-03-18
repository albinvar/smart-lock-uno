from flask import Flask, request, jsonify
import pyttsx3
import bcrypt

app = Flask(__name__)
PASSWORD = 'PASSWORD'
PASSWORD_HASH = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt()) # generate hash from the password
DEFAULT_MESSAGE = {
    'lock': "Locking the door now.",
    'unlock': "Unlocking the door now.",
    'invalid_action': "Invalid action.",
    'invalid_password': "Invalid Door Lock Password",
    'blank_password': "Blank Door Lock Password"
}

@app.route('/lock', methods=['POST'])
def lock():
    engine = pyttsx3.init()
    # Set the voice
    voices = engine.getProperty('voices')
    newVoiceRate = 140
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', voices[1].id) # Change the index to select a different voice
    action = request.form.get('action')
    if action == 'lock':
        # code to lock solenoid
        message = request.form.get('custom_message', DEFAULT_MESSAGE['lock'])
        status = "success"
    elif action == 'unlock':
        password_hash = request.form.get('password')
        if not password_hash:
            message = DEFAULT_MESSAGE['blank_password']
            status = "error"
        else:
            if not bcrypt.checkpw(PASSWORD.encode('utf-8'), password_hash.encode('utf-8')):
                message = DEFAULT_MESSAGE['invalid_password']
                status = "error"
            else:
                # code to unlock solenoid
                message = request.form.get('custom_message', DEFAULT_MESSAGE['unlock'])
                status = "success"
    else:
        message = DEFAULT_MESSAGE['invalid_action']
        status = "error"
        
    # code for voice output message
    engine.say(message)
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()
    
    response = jsonify({'message': message, 'status': status})
    response.status_code = 200 if status == "success" else 400
    return response
