import sys
from rplidar import RPLidar
import numpy as np
import cv2
from pylepton import Lepton
import time

PORT_NAME = '/dev/ttyUSB0'

timestr = ""
def captureImg(): 
    with Lepton() as l:
        a,_ = l.capture()
    cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
    np.right_shift(a, 8, a) # fit data into 8 bits
    cv2.imwrite("flir"+timestr+".jpg", np.uint8(a)) # write it!

def captureLidar():
    lidar = RPLidar(PORT_NAME)
    '''Main function'''
    outfile = open("lidar"+timestr+".txt", 'w')
    captured = 0
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measurments():
            line = '\t'.join(str(v) for v in measurment)
            outfile.write(line + '\n')
            if(captured>2):
                break
            if(measurment[0]==True):
                captured = captured+1
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    outfile.close()


def main():
    global timestr
    timestr = time.strftime("%Y%m%d-%H%M%S")
    captureLidar()
    captureImg()
    print("Captured!")

main()