int relayPin = 8;  // The pin to which the solenoid lock is connected
bool unlocked = false;

void setup() {
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == 'l') {
      digitalWrite(relayPin, HIGH);  // Activate the solenoid lock
      unlocked = true;
    } else if (receivedChar == 'u') {
      digitalWrite(relayPin, LOW);  // Deactivate the solenoid lock
      unlocked = false;
    }
  }
  
  if (unlocked) {
    // The solenoid lock is already unlocked
  } else {
    // The solenoid lock is locked
  }
}
