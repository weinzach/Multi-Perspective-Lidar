#pragma strict

import System.IO;

var points= new Array();
var prefab: GameObject;

// JavaScript
function Start () {
    ReadFile();
    drawPoints();
}

function Update () {
	
}

function drawPoints(){
    var limit = points.length;
    //limit = 10;
    for(var i = 0; i < limit; i++) {
        var point : String[];
        point = points[i];
        var x = parseFloat(point[0])/1000;
        var y = parseFloat(point[2])/1000;
        var z = parseFloat(point[1])/1000;
        var sphere = Instantiate(prefab, new Vector3 (x,y,z), Quaternion.identity);
    }
}

function ReadFile() {
    try {
        // Create an instance of StreamReader to read from a file.
        var sr = new StreamReader("TestFile.txt");
        // Read and display lines from the file until the end of the file is reached.
        var line = sr.ReadLine();
        while (line != null) {
            var lineRead : String = line;
            var strArr : String[];
            strArr= lineRead.Split(" "[0]);;
            points.Push(strArr);
            line = sr.ReadLine();
        }
        sr.Close();
    }
    catch (e) {
        // Let the user know what went wrong.
        print("The file could not be read:");
        print(e.Message);
    }
}
