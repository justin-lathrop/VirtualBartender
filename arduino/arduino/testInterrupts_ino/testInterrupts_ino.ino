volatile int state = LOW;

void setup()
{
  Serial.begin(115200);
  digitalWrite(2, HIGH);
  attachInterrupt(0, blink, CHANGE);
}

void loop()
{
  Serial.print("pin: ");
  Serial.println(digitalRead(2));
  Serial.print("\nState: ");
  Serial.println(state);
  delay(500);
}

void blink()
{
  state = !state;
}
