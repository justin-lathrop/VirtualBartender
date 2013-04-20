int sensorPin = A0;
int sensorValue = 0;

void setup() {
  Serial.begin(115200); 
}

void loop() {
  //sensorValue = 9462 / (analogRead(sensorPin) - 16.92);
  sensorValue = 4800 / (analogRead(sensorPin) - 20);
  Serial.println(sensorValue);
  delay(500);       
}
