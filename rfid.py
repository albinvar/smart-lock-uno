import RPi.GPIO as GPIO
from pi_rc522 import RFID

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# Initialize RFID reader
rfid = RFID()
rfid.init()

try:
    while True:
        # Wait for tag
        print('Waiting for tag...')
        rfid.wait_for_tag()

        # Read tag UID
        (error, tag_type) = rfid.request()
        if not error:
            (error, uid) = rfid.anticoll()
            if not error:
                uid_hex = ':'.join('{:02x}'.format(x) for x in uid)
                print('Tag UID:', uid_hex)
        rfid.stop_crypto()

finally:
    GPIO.cleanup()
