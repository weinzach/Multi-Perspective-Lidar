var config = require("./configServer.json");
var sense = require("sense-hat-led");

//Load Necessary Config Files
var node_name = config["node_name"];
var node_type = config["type"];
var node_tolerance = config["tolerance"];
var node_blinkRate = config["blink-rate"];
var batman = config["batman"];

if(batman==true){
  var Subscriber = require('cote')({'broadcast':'10.0.255.255'}).Subscriber;
}
else{
  var Subscriber = require('cote').Subscriber;
}
//LED Variables
var blink = false;
var count = 0
var status = 0;

//Intialize LEDS to Off
var X = [255, 255, 0]; // Yellow
var O = [0, 0, 0]; // OFF
var on = [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X
];
var off = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O
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
        blink = true;
        count = 0;
    }
});


//Function to Control Flashing LED Status
function ledStatus() {
    setTimeout(function() {
        if (blink==true) {
            if (status == 0) {
                sense.setPixels(on);
                status = 1;
            } else if (status == 1) {
                sense.setPixels(off);
                status = 0;
            }
            count += 1;
            if (count > node_tolerance*2) {
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
