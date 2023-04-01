import time
import config
import src.shared as shared

def rfid_processor(ser, authorized_cards):

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
                shared.voice_feedback_queue.put("Access granted, Welcome back")
                # Send signal to Arduino to unlock the lock
                ser.write(b'u')

                notification_message = f"🚪 *Door unlocked*\n\n"\
                       f"*Unlock details*\n"\
                       f"User: administrator\n"\
                       f"Unlock method: RFID Tag\n"\
                       f"Unlock duration: {config.rfid_authorized_delay} sec \n"\
                       f"Unlock action: unlock"
                shared.send_message(notification_message)

                # Keep the door unlocked for x seconds (config.rfid_authorized_delay)
                time.sleep(config.rfid_authorized_delay)

                # Send signal to Arduino to lock the lock
                ser.write(b'l')
            else:
                # Output a voice message
                shared.voice_feedback_queue.put("Card declined, please try again with a valid card")

                notification_message = f"🚪 *Card Declined*\n\n"\
                       f"*details*\n"\
                       f"Unlock method : RFID Tag\n"\
                       f"Card ID : {rfid_string} \n"\
                       f"Unlock action : unlock"
                shared.send_message(notification_message)