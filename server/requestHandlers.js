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

	process('cat ./webApp/drinks/' + getData['name'] + '.js', function(error, stdout){
		//var json = stdout;

                //console.log('json = ' + json);
                
		process('echo \''+ stdout +'\' > ../controller/Orders/'+ GLOBAL.orderNum +'.js', function(error, stdout){
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

function finishedQueue(response, postData, getData){
    console.log("Request handler 'finishedQueue' was called.");

    process('ls ../controller/OrdersCompleted', function(error, stdout){
	response.writeHead(200, {'Content-Type': 'text/plain'});
	response.end(stdout);
    });// process
}// finishedQueue

function admin(response, postData, getData){
    console.log("Request handler 'admin' was called.");

    if(getData['command']){
        process('touch ../controller/Admin/' + getData['command'] + '.command', function(error, stdout){
            response.writeHead(200, {'Content-Type': 'text/plain'});
            response.end("OK");
        });// process
    }else{
        response.writeHead(200, {'Content-Type': 'text/html'});
        var html = '<html><head><title>Admin Page</title></head>' +
                   '<body>' +
		   '<a href="/admin?command=Turn_Tray">Turn Tray</a>' +
		   '<br /><br />' +
		   '<a href="/admin?command=Mix_Drink">Mix Drink</a>' +
		   '<br /><br />' +
		   '<a href="/admin?command=Dispense_Drink_A">Dispense Drink A</a>' +
		   '<br /><br />' +
		   '<a href="/admin?command=Dispense_Drink_B">Dispense Drink B</a>' +
		   '</body></html>';

	response.end(html);
    }
}// admin

exports.start = start;
exports.makeDrink = makeDrink;
exports.image = image;
exports.recipes = recipes;
exports.getIngredients = getIngredients;
exports.drinkQueue = drinkQueue;
exports.js = js;
exports.css = css;
exports.admin = admin;
exports.finishedQueue = finishedQueue;