from flask import Flask, request, jsonify, make_response, current_app
import os
import pyttsx3
import bcrypt
import requests
import time
import shared

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
        shared.ser.write(b'l')

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
                shared.ser.write(b'u')
               
                message = request.form.get('custom_message', DEFAULT_MESSAGE['unlock'])
                status = "success"
                notification_message = f"🚪 *Door unlocked*\n\n"\
                       f"*Unlock details*\n"\
                       f"User: administrator\n"\
                       f"Unlock method: website/app\n"\
                       f"Unlock duration: until the door is locked again. \n"\
                       f"Unlock action: unlock"

                requests.post('https://lock-notification-api.lov3.pw', data={'message': notification_message})
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

@app.route('/intruders')
def intruders():
    intruders_folder = 'intruders'
    if not os.path.exists(intruders_folder):
        return jsonify(error='Intruders folder does not exist'), 404
    
    intruders_files = os.listdir(intruders_folder)
    intruders_files = sorted(intruders_files, reverse=True)  # sort in descending order
    intruders_urls = [f'/intruders/{filename}' for filename in intruders_files]
    
    return jsonify(intruders_urls)


# define the route to retrieve intruders images
@app.route('/intruders/<filename>')
def intruders_image(filename):
    intruders_folder = 'intruders'
    if not os.path.exists(intruders_folder):
        return jsonify(error='Intruders folder does not exist'), 404
    
    intruder_path = os.path.join(intruders_folder, filename)
    if not os.path.exists(intruder_path):
        return jsonify(error='Intruder not found'), 404
    
    with open(intruder_path, 'rb') as f:
        image_data = f.read()
    
    response = make_response(image_data)
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/ping')
def check_status():
    return jsonify(status='ok', message='System is connected')


if __name__ == '__main__':
    app.run(debug=True)
