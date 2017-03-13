import asyncio
from rplidar import RPLidar
import math
from concurrent.futures import ProcessPoolExecutor
import time

PORT_NAME_UNIX = '/dev/ttyUSB0'
PORT_NAME_WINDOWS = 'COM4'

count = 0
found = False
emit = 0

print('running async test')


#Algorithm to go through 2 lists to compare distances and equal angles
def motionDetect(previous,current):
        global count
        global emit
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
                emit = 1
                return True

        return False

#Main run function
def motionLidar():
        global found
        global emit
        #Intialize Variables
        firstArray = 0
        previous = []
        current = []
        lidar = RPLidar(PORT_NAME_UNIX)
        print("Starting Scan...")
        while True:
            for measurment in lidar.iter_measurments():
                if measurment[0] == True:
                #Compare every 2 Arrays
                    if(firstArray==2):
                        found = motionDetect(previous,current)
                        print(str(found)+" "+str(emit))
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

def emitter():
    global emit
    print('Waiting to Emit...')
    while True:
        time.sleep(1)
        print(str(emit))
        if(emit==1):
            emit = 0

if __name__ == "__main__":
    executor = ProcessPoolExecutor(2)
    loop = asyncio.get_event_loop()
    boo = asyncio.ensure_future(loop.run_in_executor(executor, motionLidar))
    baa = asyncio.ensure_future(loop.run_in_executor(executor, emitter))
    loop.run_forever()
