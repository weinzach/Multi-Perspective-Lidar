from rplidar import RPLidar
import math

PORT_NAME_UNIX = '/dev/ttyUSB0'
PORT_NAME_WINDOWS = 'COM4'

count = 0

#Algorithm to go through 2 lists to compare distances and equal angles
def motionDetect(previous,current):
        global count
        #Intialize Variables
        prevLength = len(previous)
        currLength = len(current)
        listLength = 0
        diffs = 0

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
        if(diffs>20):
                count = count+1
                print ("Count: "+str(count))

#Main run function        
def run():
        #Intialize Variables
        firstArray = 0
        previous = []
        current = []
        lidar = RPLidar(PORT_NAME_WINDOWS)
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

if __name__ == '__main__':
	run()
