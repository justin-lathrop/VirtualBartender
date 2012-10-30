var process = require("child_process").exec;
var querystring = require("querystring");
var fs = require("fs");

function start(response, postData, getData){
	console.log("Request handler 'start' was called.");
 
	process('cat ./webApp/index.html', function(error, stdout){
		response.writeHead(200, {"Content-Type": "text/html"});
		response.write(stdout);
		response.end();
	});
}// start

function makeDrink(response, postData, getData){
    console.log("Request handler 'makeDrink' was called.");
    
    process('./testCode/helloWorld ' + getData['name'], function(error, stdout){
        console.log('stdout: ' + stdout);

        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end(stdout);
    });
}// makeDrink

function image(response, postData, getData){
	console.log("Request handler 'image' was called.");

	var img = fs.readFileSync('./webApp/' + getData['name']);

	response.writeHead(200, {'Content-Type': 'image/png'});
	response.end(img, 'binary');
}// image

function recipes(response, postData, getData){
    console.log("Request handler 'recipes' was called.");
    
    process('cat ./webApp/recipes.html', function(error, stdout){
        //console.log('stdout: ' + stdout);

        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end(stdout);
    });// process
}// recipes

function getIngredients(response, postData, getData){
    console.log("Request handler 'getIngredients' was called.");

    process('cat ./webApp/drinks/' + getData['name'], function(error, stdout){
        response.writeHead(200, {'Content-Type': 'application/json'});
        response.end(stdout);
    });// process
}// getIngredients

exports.start = start;
exports.makeDrink = makeDrink;
exports.image = image;
exports.recipes = recipes;
exports.getIngredients = getIngredients;