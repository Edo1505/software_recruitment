unsigned long previousMillis = 0;
const long interval = 100;

void setup() {
  Serial.begin(19200);
}

void loop() {

    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;

    
    int joyValue = analogRead(A2);  // reading analog value from pin A2

   
    long motorPos = map(joyValue, 0, 1023, 818, 511);   // mapping

    
    Serial.write(0x1E);                 // instruction
    Serial.write(lowByte(motorPos));    // lower value (1° byte)
    Serial.write(highByte(motorPos));   // upper value (2° byte)
  }
}
