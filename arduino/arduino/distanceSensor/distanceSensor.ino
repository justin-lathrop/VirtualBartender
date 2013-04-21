const int sensorPin = A0;
int sensorValue = 0;
const int START = 10;
const int onpin = 8;

void setup(){
  pinMode(onpin, OUTPUT);
  digitalWrite(onpin, LOW);
}

void loop(){
  int anal = analogRead(sensorPin);
  if(anal >= 0){
    sensorValue = 4800 / (anal - 20);
    
    if((START >= sensorValue) && (0 <= sensorValue)){
      //Serial.println(sensorValue);
      digitalWrite(onpin, HIGH);
    }else{
      digitalWrite(onpin, LOW);
    }
  }
  delay(50);       
}
