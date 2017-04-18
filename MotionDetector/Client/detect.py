from rplidar import RPLidar
import math
import json
from pprint import pprint
import calendar
from datetime import datetime
import numpy as np

#Looad in Config File
with open('configClient.json') as data_file:
    config = json.load(data_file)
node_name = config["node_name"]
lidarPort = config["port"]
lidarSensitivity = config["sensitivity"]
lidarThreshold = config["threshold"]

dbId = ""

#Algorithm to go through 2 lists to compare distances and equal angles
def motionDetect(prevAngle,prevDist,currAngle,currDist):
        global count

        #Intialize Variables
        diffs = 0
        count = 0

        currAvgList = []
        currAvg = 0
        curr = (np.asarray(currAngle))

        for i in range (0,361,10):
            dat = (np.where((curr >= i) & (curr < i+11)))
            if(len(dat[0])>0):
                for j in range(0,len(dat)):
                    currAvg = currAvg + currDist[dat[0][j]]
            currAvgList.append(currAvg/10)
            currAvg = 0

        prevAvgList = []
        prevAvg = 0
        prev = (np.asarray(prevAngle))

        for i in range (0,361,10):
            dat = (np.where((prev >= i) & (prev < i+11)))
            if(len(dat[0])>0):
                for j in range(0,len(dat)):
                    prevAvg = prevAvg + prevDist[dat[0][j]]
            prevAvgList.append(prevAvg/10)
            prevAvg = 0

        for i in range(0,len(prevAvgList)):
            if((abs(prevAvgList[i]-currAvgList[i]))>lidarSensitivity):
                diffs = diffs+1

        #Print if Differences are above tolerance
        if(diffs>lidarThreshold):
            print ("Motion Found! ("+str(diffs)+")")

#Main run function
def lidarScan():
        #Intialize Variables
        firstArray = 0
        prevAngle = []
        prevDist = []
        currAngle = []
        currDist = []
        lidar = RPLidar(lidarPort)
        print('Recording measurments... Press Crl+C to stop')

        try:
                #Start Lidar Scanning
                for measurment in lidar.iter_measurments():
                        if measurment[0] == True:
                                #Compare every 2 Arrays
                                if(firstArray==2):
                                        motionDetect(prevAngle,prevDist,currAngle,currDist)
                                        prevAngle = currAngle
                                        prevDist = currDist
                                        firstArray = 0
                                else:
                                        firstArray = firstArray+1
                        #Append Data to Current Array
                                currAngle = []
                                currDist = []
                                currAngle.append(int(measurment[2]))
                                currDist.append(float(measurment[3]))
                        else:
                                currAngle.append(int(measurment[2]))
                                currDist.append(float(measurment[3]))
        except KeyboardInterrupt:
                print('Stopping...')
        #Stop Lidar
        lidar.stop()
        lidar.disconnect()

def init():
    lidarScan()

if __name__ == '__main__':
	init()
