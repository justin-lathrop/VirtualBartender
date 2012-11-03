#include <wiringPi.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(void){
	int pin = 25;
	
	printf("Beginning GPIO test with wiringPi.");

	// Check if pins are setup correctly
	if(wiringPiSetup() == -1)
		exit(1);

	// Declare pins as inputs or outputs
	pinMode(pin, OUTPUT);

	// Begin main GPIO test program
	for(;;){
		printf(", Begin main program");

		printf(", LED ON");
		digitalWrite(pin, 1);

		delay(500);

		printf(", LED OFF");
		digitalWrite(pin, 0);

		delay(500);
	}// for

	return(0);
}// main
