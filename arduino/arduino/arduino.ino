/*
 * @author: Justin Lathrop,
 *   Boreth Uy, Anthony 
 *   Madrigul, Jeffrey 
 *   Chen.
 * 
 * @param: Reads input ASCII 
 * character one by one from 
 * Serial Port.
 * 
 * @return: returns '1' for 
 * success and '0' for failure 
 * and '2' for unkown command 
 * based on input command to 
 * perform from Serial Port.
 */
#include <Stepper.h>

// Overall Program
char input = 0;

// Tray
// 1.8(degree) per step
//   360 / 1.8 = 200 steps
const double stepDegree_tray = 1.8;
const int stepsPerRevolution_tray = (int) 360 / stepDegree_tray;
Stepper myStepper_tray(stepsPerRevolution_tray, 8, 9, 10, 11);

void steps_tray(int d, int n){
  myStepper_tray.step(n);
  delay(d);
}

void degreeStep_tray(double deg, int d){
  int nStep = (int) deg / stepDegree_tray;
  steps_tray(d, nStep);
}

void moveTray(int n, int d){
  int cup = n * 60;
  degreeStep_tray(cup, d);
}

// Mixer
const double stepDegree_mixer = 7.5;
const int stepsPerRevolution = (int) 360 / stepDegree_mixer;
Stepper myStepper_mixer(stepsPerRevolution_tray, 4, 5, 6, 7);

void steps_mixer(int d, int n){
  myStepper_mixer.step(n);
  delay(d);
}

void degreeStep_mixer(double deg, int d){
  int nStep = (int) deg / stepDegree_mixer;
  steps_mixer(d, nStep);
}

void moveUp_mixer(int d){
  degreeStep_mixer(-375, d);
}

void moveDown_mixer(int d){
  degreeStep_mixer(375, d);
}

// Main Program
void setup(){
  myStepper_tray.setSpeed(10);
  myStepper_mixer.setSpeed(30);
  
  Serial.begin(115200);
}

void loop(){
  if(Serial.available() > 0){
    input = Serial.read();
    
    switch(input){
      case 'A':
        delay(2000);
        if(dispenseLiquid()){
          Serial.print('A');
          //success();
        }else{
          error();
        }
        break;
      case 'B':
        delay(2000);
        if(dispenseLiquid()){
          Serial.print('B');
          //success();
        }else{
          error();
        }
        break;
      case 'T':
        delay(2000);
        if(rotateTray()){
          Serial.print('T');
          //success();
        }else{
          error();
        }
        break;
      case 'M':
        delay(2000);
        if(mixDrink()){
          Serial.print('M');
          //success();
        }else{
          error();
        }
        break;
      default:
        unknown();
        break;
    };
    //Serial.println(input);
  }
}

/*
 *
 */
 boolean mixDrink(){
   moveUp_mixer(1000);
   moveDown_mixer(1000);
   
   return true;
 }

/*
 * Dispense Liquid into the 
 * cup below it.
 * 
 * @param:
 *    - int liquid number
 *    - int amount of servings
 * 
 * @return: true is successful 
 * false if unsuccessful.
 */
 boolean dispenseLiquid(/*int liqNum, int servings*/){
   return true;
 }

/*
 * Rotate tray to next drink 
 * position.
 * 
 * @return: true if successful 
 * false if unsuccessful.
 */
 boolean rotateTray(){
   moveTray(1, 1000);
   
   return true;
 }

/*
 * Print error character 
 * onto Serial Port.
 */
 void error(){
   Serial.print('0');
 }
 
 /*
 * Print success character 
 * onto Serial Port.
 */
 void success(){
   Serial.print('1');
 }
 
 /*
  * Print unknown character 
  * onto Serial Port.
  */
  void unknown(){
    Serial.print('2');
  }
