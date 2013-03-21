//var http = require("http");
var https = require("https");
var auth = require("http-auth");
var url = require("url");
var fs = require("fs");

var digest = auth({
        authRealm: "Login to order",
        authFile: "./htpasswd",
        authType: "digest"
});

var options = {
	key: fs.readFileSync("private-key.pem"),
	cert: fs.readFileSync("public-cert.pem")
}

function start(route, handle, port){
	function onRequest(request, response){
                digest.apply(request, response, function(username){
                    var postData = "";
                    var pathname = url.parse(request.url).pathname;
                    console.log("Request for " + pathname + " received.");

                    request.setEncoding("utf8");

                    request.addListener("data", function(postDataChunk){
                        	postData += postDataChunk;
                    });// data listener

                	request.addListener("end", function(){
            		var getData = url.parse(request.url, true).query;
            		route(handle, pathname, response, postData, getData);
                    });// end listener
                });
	}// onRequest

	https.createServer(options, onRequest).listen(port);
	console.log("Server has started listening on port " + port);
}// start

exports.start = start;
