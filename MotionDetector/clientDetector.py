from rplidar import RPLidar
import math
import json
from pprint import pprint
from pymongo import MongoClient
import calendar
from datetime import datetime

#Looad in Config File
with open('config.json') as data_file:
    config = json.load(data_file)
node_name = config["node_name"]
lidarPort = config["port"]

#Connect to Database
client = MongoClient('mongodb://localhost:27017/')
db = client['lidarDetector']
collection = db.data

count = 0
dbId = ""
result = ""

#Algorithm to go through 2 lists to compare distances and equal angles
def motionDetect(previous,current):
        global count
        global result

        d = datetime.utcnow()
        timestamp=calendar.timegm(d.utctimetuple())
        #Intialize Variables
        print(result["data"])
        prevLength = len(previous)
        currLength = len(current)
        listLength = 0
        diffs = 0
        count = 0

        #Use range of smallest lsit
        if(prevLength<currLength):
                listLength = prevLength
        else:
                listLength = currLength

        #check for differences
        for i in range(0, listLength):
                angleC = int(float(current[i].split(" ")[0]))
                angleP = int(float(previous[i].split(" ")[0]))
                distC = int(float(current[i].split(" ")[1]))
                distP = int(float(previous[i].split(" ")[1]))
                if(abs(angleC-angleP)>2):
                        if(abs(distC-distP)>20):
                                diffs = diffs+1

        #Print if Differences are above tolerance
        if(diffs>40):
            db.data.update_one({
                '_id': dbId
                },{
                    '$set': {
                        'motion': True,
                        'data': str(diffs)+","+str(timestamp)
                }
                }, upsert=False)
            result = collection.find_one({"node_name": node_name})
            print ("Motion Found! ("+str(diffs)+")")

#Main run function
def lidarScan():
        #Intialize Variables
        firstArray = 0
        previous = []
        current = []
        lidar = RPLidar(lidarPort)
        print('Recording measurments... Press Crl+C to stop')

        try:
                #Start Lidar Scanning
                for measurment in lidar.iter_measurments():
                        if measurment[0] == True:
                                #Compare every 2 Arrays
                                if(firstArray==2):
                                        motionDetect(previous,current)
                                        previous = current
                                        firstArray = 0
                                else:
                                        firstArray = firstArray+1
                        #Append Data to Current Array
                                current = []
                                current.append(str(measurment[2])+" "+str(measurment[3]))
                        else:
                                current.append(str(measurment[2])+" "+str(measurment[3]))
        except KeyboardInterrupt:
                print('Stopping...')
        #Stop Lidar
        lidar.stop()
        lidar.disconnect()

def init():
    global dbId
    global result
    print("Accessing DB...")
    client.server_info()
    result = collection.find_one({"node_name": node_name})
    if(result==None):
        print("Node "+node_name+" not found! Adding to Database...")
        result = db.data.insert_one(
        {
        "node_name": node_name,
        "motion": False,
        "data": 0
        }
        )
        dbId = result.inserted_id
        lidarScan()
    else:
        print("Node "+node_name+" found!")
        dbId = result["_id"]
        lidarScan()

if __name__ == '__main__':
	init()
