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
    
    GLOBAL.orderNum++;

	process('cat ./webApp/drinks/' + getData['name'], function(error, stdout){
		process('echo "'+ stdout +'" > ../controller/Orders/'+ GLOBAL.orderNum +'.order', function(error, stdout){
		 console.log('Order sent');

		 response.writeHead(200, {'Content-Type': 'text/plain'});
		 response.end("Order Number: "+ GLOBAL.orderNum);
		});
	});
}// makeDrink

function image(response, postData, getData){
	console.log("Request handler 'image' was called.");

	var img = fs.readFileSync('./webApp/' + getData['name']);

	response.writeHead(200, {'Content-Type': 'image/png'});
	response.end(img, 'binary');
}// image

function js(response, postData, getData){
	console.log("Request handler 'js' was called.");

    process('cat ./webApp/' + getData['name'], function(error, stdout){
        //console.log('stdout: ' + stdout);

        response.writeHead(200, {'Content-Type': 'javascript'});
        response.end(stdout);
    });// process
}// image

function css(response, postData, getData){
	console.log("Request handler 'css' was called.");

    process('cat ./webApp/' + getData['name'], function(error, stdout){
        //console.log('stdout: ' + stdout);

        response.writeHead(200, {'Content-Type': 'text/css'});
        response.end(stdout);
    });// process
}// image

function recipes(response, postData, getData){
    console.log("Request handler 'recipes' was called.");
    
    process('cat ./webApp/recipes.html', function(error, stdout){
        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end(stdout);
    });// process
}// recipes

function getIngredients(response, postData, getData){
    console.log("Request handler 'getIngredients("+ getData['name'] +")' was called.");

    process('cat ./webApp/drinks/' + getData['name'], function(error, stdout){
        response.writeHead(200, {'Content-Type': 'application/json'});
        response.end(stdout);
    });// process
}// getIngredients

function drinkQueue(response, postData, getData){
    console.log("Request handler 'drinkQueue' was called.");

    process('ls ../controller/Orders', function(error, stdout){
		response.writeHead(200, {'Content-Type': 'text/plain'});
		response.end(stdout);
    });// process
}// drinkQueue

exports.start = start;
exports.makeDrink = makeDrink;
exports.image = image;
exports.recipes = recipes;
exports.getIngredients = getIngredients;
exports.drinkQueue = drinkQueue;
exports.js = js;
exports.css = css;
