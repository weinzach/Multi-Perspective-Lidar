//Module dependencies.
var mongoose = require('mongoose');
var config = require("./configServer.json");
var converter = require('json-2-csv');
var fs = require('fs');

var options = {
    delimiter: {
        wrap: '"', // Double Quote (") character
        field: ',', // Comma field delimiter
        array: ';', // Semicolon array value delimiter
        eol: '\n' // Newline delimiter
    },
    prependHeader: true,
    sortHeader: false,
    trimHeaderValues: true,
    trimFieldValues: true,
    keys: ['diff', 'detect', 'time', 'node_name', 'node_type']
};

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

var json2csvCallback = function(err, csv) {
    if (err) throw err;
    fs.writeFile('data.csv', csv, function(err) {
        if (err) throw err;
        console.log('file saved! (data.csv)');
        process.exit();
    });
};

dataDetails.find({}, function(err, data) {
    if (err) throw err;
    console.log("retrieving data...")
    for (var i = 0; i < data.length; i++) {
      var time = parseInt(data[i].time);
      data[i].time = new Date(time);
    }
    converter.json2csv(data, json2csvCallback, options);
});
