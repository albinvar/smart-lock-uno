import pyttsx3

# Create the TTS engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
newVoiceRate = 150
engine.setProperty('rate',newVoiceRate)
engine.setProperty('voice', voices[0].id) # Change the index to select a different voice

# Speak the message
engine.say("Facial Recognition Completed!. Releasing the lock.")
engine.runAndWait()
