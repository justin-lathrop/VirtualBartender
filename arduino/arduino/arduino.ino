/*
 * @author: Justin Lathrop,
 *   Boreth Uy, Anthony
 *   Madrigul, Jeffrey
 *   Chen.
 *
 * @param: Reads input ASCII
 * character one by one from
 * Serial Port.
 *  'L': Dispense Liquid
 *   params: drink num, amount
 *  'T': move tray
 *    params: drink spots to move
 *  'D': move down mixer
 *  'U'; move up mixer
 *
 * @return: returns '1' for
 * success and '0' for failure
 * and '2' for unkown command
 * based on input command to
 * perform from Serial Port. 
 * If there is an '!' that either 
 * means the emergency stop has 
 * begun or it has just happened.
 */
#include <Stepper.h>

// Overall Program
char input = 0;
char drink = 0;
char amount = 0;
char traySpots = 0;
volatile boolean emergState = false;
boolean started = false;
const int MIXER_DISTANCE = 100;
const int PIN_TRAY[4] = {9, 10, 11, 12};
const int PIN_MIXER[4] = {15, 14, 17, 16};
const int PIN_LIQUID[7] = {20, 21, 22, 23, 24, 
    25, 26};
const int PIN_START_BTN = 7;

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
 
void moveTray(int n, int d){
  int cup = n * 60;
  degreeStep_tray(cup, d);
}
 
// Mixer
const double stepDegree_mixer = 7.5;
const int stepsPerRevolution_mixer = (int) 360 / stepDegree_mixer;
Stepper myStepper_mixer(stepsPerRevolution_mixer, PIN_MIXER[0], PIN_MIXER[1], PIN_MIXER[2], PIN_MIXER[3]);
 
void steps_mixer(int d, int n){
  myStepper_mixer.step(n);
  delay(d);
}
 
void degreeStep_mixer(double deg, int d){
  int nStep = (int) deg / stepDegree_mixer;
  steps_mixer(d, nStep);
}
 
boolean moveUp_mixer(int d){
  degreeStep_mixer(-300, d);
  return true;
}
 
boolean moveDown_mixer(int d){
  degreeStep_mixer(300, d);
  return true;
}
 
// Main Program
void setup(){
  myStepper_tray.setSpeed(10);
  myStepper_mixer.setSpeed(30);

  pinMode(PIN_EMERG_BTN, INPUT);
  digitalWrite(PIN_EMERG_BTN, HIGH);

  pinMode(PIN_START_BTN, INPUT);
  digitalWrite(PIN_START_BTN, HIGH);

  pinMode(PIN_LIQUID[0], OUTPUT);
  pinMode(PIN_LIQUID[1], OUTPUT);
  pinMode(PIN_LIQUID[2], OUTPUT);
  pinMode(PIN_LIQUID[3], OUTPUT);
  pinMode(PIN_LIQUID[4], OUTPUT);
  pinMode(PIN_LIQUID[5], OUTPUT);
  pinMode(PIN_LIQUID[6], OUTPUT);
  digitalWrite(PIN_LIQUID[0], LOW);
  digitalWrite(PIN_LIQUID[1], LOW);
  digitalWrite(PIN_LIQUID[2], LOW);
  digitalWrite(PIN_LIQUID[3], LOW);
  digitalWrite(PIN_LIQUID[4], LOW);
  digitalWrite(PIN_LIQUID[5], LOW);
  digitalWrite(PIN_LIQUID[6], LOW);

  Serial.begin(115200);
  
  // Initialize hardware interrupts
  digitalWrite(2, HIGH);
  attachInterrupt(0, emergency, LOW);

  Serial.write("Starting");
  start();
  Serial.write("Started");
}
 
void loop(){
  drink = 0;
  amount = 0;
  traySpots = 0;

  if(Serial.available() > 0){
    if(emergState == false){
      input = Serial.read();
     
      switch(input){
        case 'L':
          drink = (Serial.read() - '0');
          amount = (Serial.read() - '0');
          if((drink != 0) && (amount != 0)){
            if(dispenseLiquid(drink, amount)){
              success();
            }else{
              error();
            }
          }else{
            error();
          }
          break;
        case 'T':
          traySpots = (Serial.read() - '0');
          if(traySpots > 0){
            if(rotateTray(traySpots)){
              success();
            }else{
              error();
            }
          }else{
            error();
          }
          break;
        case 'D':
          if(moveDown_mixer(MIXER_DISTANCE)){
            success();
          }else{
            error();
          }
          break;
        case 'U':
          if(moveUp_mixer(MIXER_DISTANCE)){
            success();
          }else{
            error();
          }
          break;
        default:
          unknown();
          break;
      };
      //Serial.println(input);
    }else{
      Serial.write('!');
      start();
    }
  }// if
}

/*
 * Interrupt handler for PIN0 
 * will send pause signal to 
 * controller over Serial and 
 * stop after current step.
 * 
 * This is done by setting 
 * the 'emergState' variable 
 * to boolean true.
 */
void emergency(){
  emergState = true;
}

/*
 * After emergency interrupt 
 * or start, will wait until 
 * start button is pressed. 
 * After pressed will send to 
 * controller to start the 
 * current process again.
 */
void start(){
  while(1){
    if(digitalRead(PIN_START_BTN) == LOW){
      emergState = false;
      if(started){ Serial.write('!'); }
      started = true;
      break;
    }
    delay(10);
  }
}

/*
 * Dispense liquid into the
 * cup below it.  Liquid 
 * number is the pin from 
 * drink left to right 
 * when looking at it from 
 * the front.
 *
 * @param:
 *    - int liquid number
 *    - int amount of servings
 *
 * @return: true is successful
 * false if unsuccessful.
 */
boolean dispenseLiquid(int liquid, int servings){
  int time = 0;

  if((liquid >= 1) && (amount >= 1)){
    // Calculate time given serving amount
    

    digitalWrite(PIN_LIQUID[liquid], HIGH);
    delay(time);
  }else{
    return false;
  }

  return true;
}
 
/*
 * Rotate tray to next drink
 * position.
 *
 * @params:
 *   - int spots
 *
 * @return: true if successful
 * false if unsuccessful.
 */
boolean rotateTray(int spots){
   moveTray(spots, 0);
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
