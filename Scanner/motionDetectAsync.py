import asyncio
from rplidar import RPLidar
import math

PORT_NAME_UNIX = '/dev/ttyUSB0'
PORT_NAME_WINDOWS = 'COM4'

count = 0
found = False

#Algorithm to go through 2 lists to compare distances and equal angles
@asyncio.coroutine
def motionDetect(previous,current):
        global count
        global found
        #Intialize Variables
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
                found = True
                print ("Motion Found! ("+str(diffs)+")")

#Main run function
@asyncio.coroutine
def motionLidar():
        #Intialize Variables
        firstArray = 0
        previous = []
        current = []
        lidar = RPLidar(PORT_NAME_UNIX)
        while True:
            yield #Start Lidar Scanning
            print('Starting Scan...')
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

        #Stop Lidar
        lidar.stop()
        lidar.disconnect()

@asyncio.coroutine
def emitter():
    global found
    print('Waiting to Emit...')
    while True:
        yield
        if(found==True):
            print("Emtting...")
            found = False

boo_task = asyncio.async(emitter())
baa_task = asyncio.async(motionLidar())

loop = asyncio.get_event_loop()
loop.run_forever()
