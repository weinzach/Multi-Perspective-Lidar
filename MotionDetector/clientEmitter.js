
// Retrieve
var MongoClient = require('mongodb').MongoClient;

var collectionData;
// Connect to the db
MongoClient.connect("mongodb://localhost:27017/lidarDetector", function(err, db) {
  if(!err) {
    console.log("We are connected");
    collectionData = db.collection('data');
    var cursor = collectionData.find({"node_name" : "lidarDetector1"});
    cursor.each(function(err, doc) {
      if(err)
          throw err;
          if(doc==null)
            console.log("Node lidarDector1 not found!");
            return;

          console.log("node found:");
          console.log(doc);
        });
    }
});
