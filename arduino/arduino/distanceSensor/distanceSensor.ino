int sensorPin = A0;
int sensorValue = 0;

void setup() {
  Serial.begin(115200); 
}

void loop() {
  //sensorValue = 9462 / (analogRead(sensorPin) - 16.92);
  int anal = analogRead(sensorPin);
  sensorValue = 4800 / (anal - 20);
  Serial.println(sensorValue);
  Serial.println(anal);
  Serial.println("=====");
  delay(2000);       
}
