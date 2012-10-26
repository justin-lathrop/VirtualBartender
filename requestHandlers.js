var process = require("child_process").exec;
var querystring = require("querystring");

function start(response, postData, getData){
	console.log("Request handler 'start' was called.");

	process('~/SeniorProject/testCode/helloWorld ' + getData['name'], function(error, stdout, stderr){
		console.log('stdout: ' + stdout);
		var body = '<html><head><meta http-equiv="Content-type" content="text/html; charset=UTF-8" /></head>' + 
			   '<body>' +
				'C Program says: ' + stdout +
			   '</body></html>';

		response.writeHead(200, {"Content-Type": "text/html"});
		response.write(body);
		response.end();
	});// child
}// start

exports.start = start;
