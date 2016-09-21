import sys
from rplidar import RPLidar
import RPi.GPIO as GPIO

STEPPER_PIN = 23
PORT_NAME = '/dev/ttyUSB0'



GPIO.setmode(GPIO.BCM)

GPIO.setup(STEPPER_PIN, GPIO.OUT)
GPIO.output(STEPPER_PIN, False)
x = 0

def step_motor():
       	GPIO.output(23, True)
        GPIO.output(23, False)
	
def run():
        try:
		step_motor()
        except KeyboardInterrupt:
                print('Stopping')

if __name__ == '__main__':
        run()

