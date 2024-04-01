from sinric import SinricPro, SinricProConstants
import asyncio
import threading
import src.shared as shared
import config

# Add Sinric Credentials
appKey = '59011c51-4e93-49e0-85b4-f9269b1097ff'
secretKey = '414b0890-caa8-499d-ad86-2fb24b5038f6-b0a5a748-0653-4aa2-89a2-b0eaa3a4c5df'
lockId = '65c78868ccc93539a137533c'

def Events():
    while True:
        # Select as per your requirements
        # REMOVE THE COMMENTS TO USE
        # client.event_handler.raiseEvent(lockId, 'setLockState', data={'state': 'LOCKED'})
        # client.event_handler.raiseEvent(lockId, 'setLockState', data={'state': 'UNLOCKED'})
        pass

event_callback = {
    'Events': Events
}

def lock_state(device_id, state):
    print(f'Lock state: {state}')
    if state == 'lock':
        message = "The door has been locked."
        shared.ser.write(b'l')
        return True, state
    elif state == 'unlock':
        shared.ser.write(b'u')
        message = "The door has been unlocked."
    # code for voice output message
    shared.voice_feedback_queue.put(message)
    return True, state


callbacks = {
    SinricProConstants.SET_LOCK_STATE: lock_state
}

loop = asyncio.get_event_loop()

def initialize_sinric(shared_ser):
    try:
        # Initialize Sinric
        client = SinricPro(appKey, [lockId], callbacks, enable_log=False, restore_states=True, secret_key=secretKey)
        print('SinricPro is connected')
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        print("Sinric initialization interrupted.")
        loop.stop()
        loop.close()