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
 *  'B': wait for start button
 *  'P': parallel dispensing
 *    params: <14 bytes drink 
 *              and servings>
 *  'R': reset tray
 *
 * @return: returns '1' for
 * success and '0' for failure
 * and '2' for unkown command
 * based on input command to
 * perform from Serial Port. 
 * If there is an '!' that either 
 * means the emergency stop has 
 * begun or it has just started.
 */
#include <Stepper.h>

// Overall Program
char input = 0;
int drink = 0;
int amount = 0;
int traySpots = 0;
int i = 0;
char drinks[7] = {'a', 'a', 'a', 'a', 'a', 'a', 'a'};
volatile boolean emergState = false;
boolean started = false;
const int MIXER_DISTANCE = 100;
const int PIN_TRAY[4] = {14, 15, 16, 17};
const int PIN_LIQUID[7] = {41, 43, 45, 47, 49, 51, 46};
const int PIN_START_BTN = 7;
const int PIN_EMERG_BTN = 2;
const int PHOTO_SENSOR_PIN = A1;
const int PHOTO_SENSOR_LIMIT = 700;

// Trayd
// 1.8(degree) per step
//   360 / 1.8 = 200 steps
const double stepDegree_tray = 1.8;
const int stepsPerRevolution_tray = (int) 360 / stepDegree_tray;
Stepper myStepper_tray(stepsPerRevolution_tray, PIN_TRAY[0], PIN_TRAY[1], PIN_TRAY[2], PIN_TRAY[3]);

void steps_tray(int d, int n){
  int i = 0;

  while(1){
    if((i >= n) || (emergState)){ break; }
    myStepper_tray.step(1);
    i += 1;
  }
}

void degreeStep_tray(double deg, int d){
  int nStep = (int) deg / stepDegree_tray;
  steps_tray(d, nStep);
}
 
void moveTray(int n, int d){
  int cup = n * 60;
  degreeStep_tray(cup, d);
}
 
// Main Program
void setup(){
  // Set up motor speeds
  myStepper_tray.setSpeed(15);

  // Set up buttons
  pinMode(PIN_START_BTN, INPUT);
  digitalWrite(PIN_START_BTN, HIGH);
  pinMode(PIN_EMERG_BTN, INPUT);
  digitalWrite(PIN_EMERG_BTN, HIGH);

  // Set up dispensor pins
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

  // Begin listening on serial
  Serial.begin(115200);
  
  // Initialize hardware interrupts
  pinMode(2, INPUT);
  digitalWrite(2, HIGH);
  attachInterrupt(0, emergency, LOW);

  // Wait for "start" button to be pressed
  start();
}
 
void loop(){
  if((digitalRead(PIN_EMERG_BTN) == LOW) || (emergState)){
    Serial.write('!');
    start();
  }

  i = 0;
  drink = 0;
  amount = 0;
  traySpots = 0;

  if(Serial.available() > 0){
    if(emergState == false){
      input = Serial.read();
     
      switch(input){
        case 'R':
          if(resetTray()){
            success();
          }else{
            error();
          }
          break;
        case 'P':
          for(i = 0; i < 7; i++){
            if(emergState){
              break;
            }else{
              drinks[i] = getChar();
            }
          }
          if(emergState){ break; }
          amount = getInt();
          if(parallel(drinks, amount)){
            success();
          }else{
            error();
          }
          break;
        case 'L':
          if(emergState){ break; }
          drink = getInt();
          if(emergState){ break; }
          amount = getInt();
          if(emergState){ break; }
          if((drink < 7) && (amount != 0)){
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
          if(emergState){ break; }
          traySpots = getInt();
          if(emergState){ break; }
          if(traySpots > 0){
            if(emergState){ break; }
            if(rotateTray(traySpots)){
              if(emergState){ break; }
              success(); 
            }else{
              error();
            }
          }else{
            error();
          }
          break;
        case 'B':
          if(emergState){ break; }
          start();
          success();
          break;
        default:
          unknown();
          break;
      };
    }// if
  }// if
}// loop

/*
 * Using millis function to get 
 * current time in milliseconds 
 * since startup in order to 
 * busy wait for either emerg 
 * button press or time to run 
 * out.
 * 
 * @return: true is no emerg 
 *   button press, false is not
 */
boolean Delay(int time){
  unsigned long startMilli = millis();
  int diff = 0;
  unsigned long currentMilli = 0.0;
  while(1){
    if(emergState){
      return false;
    }else{
      if(diff >= time){
        break;
      }else{
        currentMilli = millis();
        diff = (currentMilli - startMilli);
      }
    }
  }

  return true;
}

/*
 * Spins tray until photosensor 
 * detects trigger on the tray.
 * 
 * @return: true if successful and 
 *   false if unseccessful/emerg
 */
boolean resetTray(){
  int count = 0;
  while(1){
    if(emergState) return false;
    count++;
    if(count >= 240){
      myStepper_tray.step(-3);
      break;
    }

    if(analogRead(A1) > PHOTO_SENSOR_LIMIT){
      return true;
    }else{
      //degreeStep_tray(1, 0);
      //steps_tray(3, 0);
      myStepper_tray.step(1);
    }
  }

  return false;
}

/*
 * Given an array of drinks in 
 * order from 0 to 7 dispense 
 * amount for each in "||".
 * 
 * @param:
 *   - char * (array of drinks)
 *     - all are '1' or '0'
 *   - int amount for all drinks 
 *     to be served at once
 * 
 * @return:
 *   - boolean if successful
 */
boolean parallel(char *drinks, int amount){
  if(emergState) return false;
  int i = 0;
  double time = getTime(amount);
  
  for(i = 0; i < 7; i++){
    if((drinks[i] != '1') && (drinks[i] != '0')){
      for(i = 0; i < 7; i++){
        digitalWrite(PIN_LIQUID[i], LOW);
      }
      return false;
    }

    if(drinks[i] == '1'){
      digitalWrite(PIN_LIQUID[i], HIGH);
    }else{
      digitalWrite(PIN_LIQUID[i], LOW);
    }
  }

  Delay(time * 1000);
  //Delay(amount * 1000);

  for(i = 0; i < 7; i++){
    digitalWrite(PIN_LIQUID[i], LOW);
  }
  return true;
}

/*
 * Wait for serial input 
 * then parse byte into an 
 * integer.
 * 
 * @return: Serial input integer, 
 *   or -1 is emergState
 */
int getInt(){
  int in = 0;
  while(1){
    if(emergState){
      return(-1);
    }else if(Serial.available() > 0){
      in = (Serial.read() - '0');
      break;
    }
    Delay(10);
  }
  return(in);
}

/*
 * Wait for serial input 
 * then parse byte into a 
 * char.
 * 
 * @return: Serial input char 
 *   or '-' is emergency.
 */
char getChar(){
  while(1){
    if(emergState){
      return '-';
    }else if(Serial.available() > 0){
      return Serial.read();
    }
    Delay(10);
  }
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
      flushSerialInput();
      emergState = false;
      //if(!started){ Serial.write('!'); }
      Serial.write('!');
      started = true;
      break;
    }
    Delay(10);
  }
}

/*
 * Clears all input data on 
 * the serial bus.  Does 
 * not care about emergState.
 */
void flushSerialInput(){
  while(Serial.available() > 0){
    Serial.read();
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
  if(emergState) return false;

  if((liquid >= 0) && (amount >= 1)){
    digitalWrite(PIN_LIQUID[liquid], HIGH);
    Delay(getTime(amount) * 1000.0);
    //Delay(amount * 1000);
    digitalWrite(PIN_LIQUID[liquid], LOW);
  }else{
    return false;
  }

  return true;
}

/*
 * Calculate the amount of time to 
 * Delay for a specific serving 
 * size.
 * 
 * @param:
 *   - int servings/amount
 * 
 * @return:
 *   - double time to Delay (seconds)
 */
double getTime(int amount){
  if(emergState) return false;

  double servingSize = 44.36;
  double servingSpeed = 12.5;

  return ((amount * servingSize) / servingSpeed);
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
  if(emergState) return false;

   moveTray(spots, 0);
   return true;
}
 
/*
 * Print error character
 * onto Serial Port.
 */
void error(){
  if(emergState){ return; }
  Serial.print('0');
}
 
/*
 * Print success character
 * onto Serial Port.
 */
void success(){
  if(emergState){ return; }
   Serial.print('1');
}
 
/*
 * Print unknown character
 * onto Serial Port.
 */
void unknown(){
  if(emergState){ return; }
  Serial.print('2');
}

