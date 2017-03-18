//Module dependencies.
var mongoose = require('mongoose');
var config = require("./configClient.json");

//Load Necessary Config Files
var node_name = config["node_name"];
var node_type = config["type"];
var batman = config["batman"];

if(batman==true){
  var Publisher = require('cote')({'broadcast': '10.0.255.255'}).Publisher;
  console.log("using batman...");
}
else{
  var Publisher = require('cote').Publisher;
}

// Instantiate a new Publisher component.
var randomPublisher = new Publisher({
    name: node_name,
    broadcasts: ['detectors']
});

// Wait for the publisher to find an open port and listen on it.
randomPublisher.on('ready', function() {
    ready = 1;
});


var dbId = "";
var nodeData = [];

//Connect to Database
mongoose.connection.on('open', function(ref) {
    console.log('Connected to mongo server.');
});
mongoose.connection.on('error', function(err) {
    console.log('Could not connect to mongo server!');
    console.log(err);
});
mongoose.connect('mongodb://localhost/lidarDetector');
var Schema = mongoose.Schema;

//Data Schema
var dataDetail = new Schema({
    node_name: String,
    motion: Boolean,
    data: String
}, {
    collection: 'data'
});

//Create MongoDB models
var dataDetails = mongoose.model('data', dataDetail);


//Emit on Mesh
function emitter() {
    nodeData.push(node_name);
    nodeData.push(node_type);
    console.log("emit");
    randomPublisher.publish("detectors", nodeData);
    dataDetails.update({
        _id: dbId
    }, {
        motion: false
    }, function(err, affected, resp) {
        return;
    });

}

//Check for DB Entry
function checkDB() {
    dataDetails.findOne({
            'node_name': node_name
        },
        function(err, node) {
            if (err) {
                return console.log(err);
            }
            if (!node) {
                return console.log("Node not found! Try reinitializing with the clientDetector.py");
            }
            dbId = node.id;
            nodeData = node.data.split(",");
            if (node.motion == true) {
                emitter();
            }
        });
}

function init() {
    //Check Database Every Half Second for Changes
    setTimeout(function() {
        checkDB();
        init();
    }, 500)
}

init(); //  start the loop
