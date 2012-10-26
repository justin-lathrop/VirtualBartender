var http = require("http");
var url = require("url");

function start(route, handle, port){
	function onRequest(request, response){
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
	}// onRequest

	http.createServer(onRequest).listen(port);
	console.log("Server has started listening on port " + port);
}// start

exports.start = start;
