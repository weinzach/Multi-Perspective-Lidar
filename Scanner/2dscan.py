import sys
from rplidar import RPLidar
import math

# = '/dev/ttyUSB0'
PORT_NAME = 'COM4'

def run():
        lidar = RPLidar(PORT_NAME)
        outfile = open('lidardata.txt', 'w')
        try:
                print('Recording measurments... Press Crl+C to stop.')
                for measurment in lidar.iter_measurments():
                        if(measurment[3]!=0):
                                x = math.cos(measurment[2])*measurment[3]
                                y = math.sin(measurment[2])*measurment[3]
                                line = str(x)+" "+str(y)
                                outfile.write(line + '\n')
        except KeyboardInterrupt:
                print('Stopping')
        lidar.stop()
        lidar.disconnect()
        outfile.close()

if __name__ == '__main__':
	run()
