#include <Stepper.h>

const int PIN_TRAY[4] = {7, 6, 5, 4};

// Trayd
// 1.8(degree) per step
//   360 / 1.8 = 200 steps
const double stepDegree_tray = 1.8;
const int stepsPerRevolution_tray = (int) 360 / stepDegree_tray;
Stepper myStepper_tray(stepsPerRevolution_tray, PIN_TRAY[0], PIN_TRAY[1], PIN_TRAY[2], PIN_TRAY[3]);

void steps_tray(int d, int n){
  myStepper_tray.step(n);
  delay(d);
}

void degreeStep_tray(double deg, int d){
  int nStep = (int) deg / stepDegree_tray;
  steps_tray(d, nStep);
}

void setup() {
  Serial.begin(9600);
}

int detect(int d){
  int state = 0;
  
  if (analogRead(A5) > 700)
     state = 1;
 
  delay(d);
  return state; 
}

void resetTray(){ 
  while ( detect(10) != 1)
    steps_tray(10, 1); 
    
  steps_tray(10, 1); 
    
  delay(1000); 
}

void moveTray(int n, int d){
  int cup = n * 60;
  degreeStep_tray(cup, d);
}

void command(){
  char c =   Serial.read();
  Serial.println(c);
  switch(c){
    case 'a':  resetTray(); break;
    case 'b':  moveTray(1,10); break;
    case 'c':  moveTray(2,10); break;
  }
  
  delay(1000);
}

void loop() {
  command();
  delay(5000);
}
