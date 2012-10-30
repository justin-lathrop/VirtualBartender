var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.start;
handle["/makeDrink"] = requestHandlers.makeDrink;
handle["/image"] = requestHandlers.image;
handle["/recipes"] = requestHandlers.recipes;
handle["/getIngredients"] = requestHandlers.getIngredients;

server.start(router.route, handle, process.argv[2]);
