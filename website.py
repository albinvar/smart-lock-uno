from flask import Flask, request, jsonify
import pyttsx3

app = Flask(__name__)

@app.route('/lock', methods=['POST'])
def lock():
    engine = pyttsx3.init()
    # Set the voice
    voices = engine.getProperty('voices')
    newVoiceRate = 140
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', voices[1].id) # Change the index to select a different voice
    password = request.form.get('password')
    if password == 'PASSWORD':
        action = request.form.get('action')
        if action == 'lock':
            # code to lock solenoid
            message = "Locking the door now."
            status = "success"
        elif action == 'unlock':
            # code to unlock solenoid
            message = "Unlocking the door now."
            status = "success"
        else:
            message = "Invalid action."
            status = "error"
    else:
        message = "Invalid password."
        status = "error"
    # code for voice output message
    engine.say(message)
    engine.runAndWait()
    response = jsonify({'message': message, 'status': status})
    response.status_code = 200 if status == "success" else 400
    return response
