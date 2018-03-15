import numpy as np
import cv2
from pylepton import Lepton
import time

def captureImg():
	with Lepton() as l:
		a,_ = l.capture()
	cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
	np.right_shift(a, 8, a) # fit data into 8 bits
	timestr = time.strftime("%Y%m%d-%H%M%S")
	cv2.imwrite("output"+timestr+".jpg", np.uint8(a)) # write it!
	
def captureArray():
	with Lepton() as l:
		a,_ = l.capture()
	cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
	np.right_shift(a, 8, a) # fit data into 8 bits
	timestr = time.strftime("%Y%m%d-%H%M%S")
	print(len(a.tolist()))
        np.savetxt("output"+timestr+".csv", a, delimiter=",")

def main():
	captureImg()
	captureArray()
	print("Captured!")

main()
