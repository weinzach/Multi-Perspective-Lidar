//Module dependencies.
var mongoose = require('mongoose');
var config = require("./configServer.json");
var sense = require("sense-hat-led");


//Connect to Database
mongoose.connection.on('open', function(ref) {
    console.log('Connected to mongo server.');
});
mongoose.connection.on('error', function(err) {
    console.log('Could not connect to mongo server!');
    console.log(err);
});
mongoose.connect('mongodb://localhost/lidarServer');
var Schema = mongoose.Schema;

//Data Schema
var dataDetail = new Schema({
    diff: String,
    detect: String,
    time: String,
    node_name: String,
    node_type: String
}, {
    collection: 'data'
});
//Create MongoDB models
var dataDetails = mongoose.model('data', dataDetail);

//Load Necessary Config Files
var node_name = config["node_name"];
var node_type = config["type"];
var node_tolerance = config["tolerance"];
var node_blinkRate = config["blink-rate"];
var batman = config["batman"];

if (batman == true) {
    console.log("using batman...");
    var Subscriber = require('cote')({
        'broadcast': '10.0.255.255'
    }).Subscriber;
} else {
    var Subscriber = require('cote').Subscriber;
}
//LED Variables
var blink = false;
var count = 0
var status = 0;

//Intialize LEDS to Off
var X = [255, 255, 0]; // Yellow
var O = [0, 0, 0]; // OFF
var R = [255, 0, 0]; // RED
var on = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, R
];
var off = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, R
];
sense.setPixels(off);

//Create Subscriber
var batSubscriber = new Subscriber({
    name: 'LED Server',
    subscribesTo: ['detectors']
});

//Listen for Lidar Announcement
batSubscriber.on('detectors', function(req) {
    console.log('Recieved: ', req);
    if (req[3] != node_name) {
        var dataReq = new dataDetails({
            diff: req[0],
            detect: req[1],
            time: req[2],
            node_name: req[3],
            node_type: req[4]
        });
        dataReq.save(function(err, dataReq) {
            if (err) return console.error(err);
        });
        blink = true;
        count = 0;
    }
});


//Function to Control Flashing LED Status
function ledStatus() {
    setTimeout(function() {
        if (blink == true) {
            if (status == 0) {
                sense.setPixels(on);
                status = 1;
            } else if (status == 1) {
                sense.setPixels(off);
                status = 0;
            }
            count += 1;
            if (count > node_tolerance * 2) {
                blink = false;
                count = 0;
            }
        } else {
            sense.setPixels(off);
            status = 0;
            count = 0;
        }
        ledStatus();
    }, node_blinkRate);
}

//Start LED Control
ledStatus();
