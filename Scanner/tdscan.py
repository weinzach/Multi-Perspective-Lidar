import sys
from rplidar import RPLidar
import RPi.GPIO as GPIO

#Toggle for continous scanning
Loop = False
#390 is equivalent to 1 complete roatation
MAX_STEPS = 390

STEPPER_PIN = 23
PORT_NAME = '/dev/ttyUSB0'

GPIO.setmode(GPIO.BCM)

GPIO.setup(STEPPER_PIN, GPIO.OUT)
GPIO.output(STEPPER_PIN, False)

def step_motor():
	GPIO.output(23, True)
	GPIO.output(23, False)


def run():
	lidar = RPLidar(PORT_NAME)
	stepper_position = 0
	outfile = open('lidardata.txt', 'w')
	try:
                print('Recording measurments... Press Crl+C to stop.')
		for measurment in lidar.iter_measurments():
			if measurment[0] == True:
				step_motor()
				stepper_position +=1
			measurment = measurment + (stepper_position,)
			line = '\t'.join(str(v) for v in measurment)
			outfile.write(line + '\n')
			if(stepper_position==MAX_STEPS):
				print("Cycle Complete")
				stepper_position = 0
				if(Loop==False):
					print("Stopping")
					break
	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()
	outfile.close()

if __name__ == '__main__':
	run()
			
