//Module dependencies.
var mongoose = require('mongoose');
var config = require("./config.json");

//Load Necessary Config Files
var node_name = config["node_name"];
var batman = config["batman"];

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
var dataDetails = mongoose.model('userInfo', dataDetail);

//Check for DB Entry
function checkDB() {
    dataDetail.findOne({
            'node_name': node_name
        },
        function(err, node) {
            if (err) {
                return console.log(err);
            }
            if (!node) {
                console.log("Node not found! Try reinitializing with the clientDetector.py");
            }
            console.log(node);
        });
}

function init () {
  //Check Database Every Half Second for Changes
   setTimeout(function () {
      checkDB();
   }, 500)
}

init();                      //  start the loop
