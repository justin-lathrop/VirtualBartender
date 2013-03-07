function route(handle, pathname, response, postData, getData){
	console.log("About to route a request for " + pathname);

	if(typeof handle[pathname] === "function"){
		handle[pathname](response, postData, getData);
	}else{
		console.log("No request handler found for " + pathname);

		response.writeHead(404, {"Content-type": "text/plain"});
		response.write("404 Not found.");
		response.end();
	}// else
}// route

exports.route = route;