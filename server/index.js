var p = require("child_process").exec;
var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.start;
handle["/makeDrink"] = requestHandlers.makeDrink;
handle["/image"] = requestHandlers.image;
handle["/recipes"] = requestHandlers.recipes;
handle["/getIngredients"] = requestHandlers.getIngredients;
handle["/drinkQueue"] = requestHandlers.drinkQueue;
handle["/js"] = requestHandlers.js;
handle["/css"] = requestHandlers.css;

GLOBAL.orderNum = 0;
GLOBAL.orderQueue = [];

process.on('SIGINT', function(){
	console.log('\n\nCleaning up Server then shutting down.\n\n');

	p('rm -f ./Orders/*.order; rm -f ./CurrentOrders/*.order; rm -f ./CompletedOrders/*.order', function(){});

	process.exit();
});

server.start(router.route, handle, process.argv[2]);
