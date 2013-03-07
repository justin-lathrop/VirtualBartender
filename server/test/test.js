var gpio = require('rpi-gpio');

var pin = 7, delay = 1500, count = 0, max = 4;

// Set up listener for pin value changing
gpio.on('change', function(channel, value){
	console.log('Channel ' + channel + ' value is now ' + value);
});

// Setup pin <number> as DIR_IN or DIR_OUT
gpio.setup(pin, gpio.DIR_OUT, on);

// Is first function run after setting up pin mode
function on(){
	if(count >= max){
		gpio.destroy(function(){
			console.log('Closed pins, now exited');
			return process.exit(0);
		});
	}

	// Turn on LED then after delay call function 'off'
	setTimeout(function(){
		gpio.write(pin, 1, off);
		count++;
	}, delay);
}// on

function off(){
	// Turn off the pin <number>
	setTimeout(function(){
		gpio.write(pin, 0, on);
	}, delay);
}// off
