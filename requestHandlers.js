var process = require("child_process").exec;
var querystring = require("querystring");

function start(response, postData, getData){
	console.log("Request handler 'start' was called.");
 
	process('cat ./webApp/index.html', function(error, stdout){
		response.writeHead(200, {"Content-Type": "text/html"});
		response.write(stdout);
		response.end();
	});
}// start

function helloWorld(response, postData, getData){
    console.log("Request handler 'helloWorld' was called.");
    
    process('./testCode/helloWorld ' + getData['name'], function(error, stdout){
        console.log('stdout: ' + stdout);

        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end(stdout);
    });
}// helloWorld

exports.start = start;
exports.helloWorld = helloWorld;
