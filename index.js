var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.start;
handle["/helloWorld"] = requestHandlers.helloWorld;
handle["/image"] = requestHandlers.image;
handle["/recipes"] = requestHandlers.recipes;

server.start(router.route, handle, process.argv[2]);
