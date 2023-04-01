import time
import pyttsx3
import config
import src.shared as shared

def rfid_processor(ser, authorized_cards):
    
    engine = pyttsx3.init()
    
    # Set the voice
    voices = engine.getProperty('voices')
    engine.setProperty('rate', config.voice_rate)
    engine.setProperty('voice', voices[config.voice].id)  # Change the index to select a different voice

    while True:
        # Read data from serial port
        rfid_string = ser.readline().decode().strip()
        print(rfid_string)
        if rfid_string.startswith('Card detected:'):
            # Extract the card ID from the string
            card_id = rfid_string.split(' ')[-1]
            # Check if the card is authorized
            if card_id in authorized_cards:
                # Output a voice message
                engine.say("Access granted")
                engine.runAndWait()
                # Send signal to Arduino to unlock the lock
                ser.write(b'u')

                notification_message = f"🚪 *Door unlocked*\n\n"\
                       f"*Unlock details*\n"\
                       f"User: administrator\n"\
                       f"Unlock method: RFID Tag\n"\
                       f"Unlock duration: 5 sec \n"\
                       f"Unlock action: unlock"
                shared.send_message(notification_message)

                # Wait for 5 seconds
                time.sleep(5)

                # Send signal to Arduino to lock the lock
                ser.write(b'l')
            else:
                # Output a voice message
                engine.say("Access denied")
                engine.runAndWait()
                notification_message = f"🚪 *Card Declined*\n\n"\
                       f"*details*\n"\
                       f"Unlock method: RFID Tag\n"\
                       f"Card ID : 12345 \n"\
                       f"Unlock action: unlock"
                shared.send_message(notification_message)