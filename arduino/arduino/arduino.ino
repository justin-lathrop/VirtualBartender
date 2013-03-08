/*
 * @author: Justin Lathrop
 * 
 * @param: Reads input ASCII 
 * character one by one from 
 * Serial Port.
 * 
 * @return: returns '1' for 
 * success and '0' for failure 
 * based on input command to 
 * perform from Serial Port.
 */
char input = 0;

void setup(){
  Serial.begin(115200);
}

void loop(){
  if(Serial.available() > 0){
    input = Serial.read();
    
    switch(input){
      case 'A':
        delay(2000);
        if(rotateTray()){
          success();
        }else{
          error();
        }
        break;
      case 'B':
        delay(2000);
        if(dispenseLiquid(0, 0)){
          success();
        }else{
          error();
        }
      default:
        unknown();
        break;
    };
    //Serial.println(input);
  }
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
 boolean dispenseLiquid(int liqNum, int servings){
   return true;
 }

/*
 * Rotate tray to next drink 
 * position.
 * 
 * @return: true is successful 
 * false if unsuccessful.
 */
 boolean rotateTray(){
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
