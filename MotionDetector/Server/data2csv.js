var json2csv = require('json2csv');
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
    time: String,
    node_name: String,
    node_type: String
}, {
    collection: 'data'
});
//Create MongoDB models
var dataDetails = mongoose.model('data', dataDetail);

// get all the users
dataDetails.find({}, function(err, data) {
  if (err) throw err;

  var result = json2csv({ fields: data });
  console.log(result);
});
