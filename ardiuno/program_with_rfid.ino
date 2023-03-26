#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
#define RELAY_PIN 2

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance.

bool unlocked = false;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  Serial.begin(9600);

  SPI.begin();          // Initialize SPI bus.
  mfrc522.PCD_Init();   // Initialize MFRC522 card reader.
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();
    if (receivedChar == 'l') {
      digitalWrite(RELAY_PIN, HIGH);  // Activate the solenoid lock
      unlocked = false;
    } else if (receivedChar == 'u') {
      digitalWrite(RELAY_PIN, LOW);  // Deactivate the solenoid lock
      unlocked = true;
    }
  }

  if (unlocked) {
    // The solenoid lock is already unlocked
  } else {
    // The solenoid lock is locked
    // Check for new cards.
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
      // Get card UID.
      String cardUID = "";
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        cardUID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        cardUID += String(mfrc522.uid.uidByte[i], HEX);
      }

      // Print card UID to serial monitor.
      Serial.println("Card detected: " + cardUID);

      // Halt PICC.
      mfrc522.PICC_HaltA();
      // Stop encryption on PCD.
      mfrc522.PCD_StopCrypto1();
   
    }
  }
}