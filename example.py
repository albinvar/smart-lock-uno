import pyttsx3

# Create the TTS engine
engine = pyttsx3.init()

# Set the voice
voices = engine.getProperty('voices')
newVoiceRate = 140
engine.setProperty('rate',newVoiceRate)
engine.setProperty('voice', voices[1].id) # Change the index to select a different voice

# Speak the message
engine.say("Facial Features Identified!.   Welcome back Albin Varghese!,  The door locks will be released soon.   The door will be locked back in 60 seconds..")
engine.runAndWait()
