var process = require("child_process").exec;
var querystring = require("querystring");

function start(response, postData, getData){
	console.log("Request handler 'start' was called.");

	process('~/SeniorProject/VirtualBartender/testCode/helloWorld ' + getData['name'], function(error, stdout, stderr){
		console.log('stdout: ' + stdout);
		var cProg_output = stdout;
		
		process('cat ~/SeniorProject/VirtualBartender/webApp/index.html', function(error, stdout){
			response.writeHead(200, {"Content-Type": "text/html"});
			response.write(stdout);
			response.end();
		});
	});// child
}// start

exports.start = start;
