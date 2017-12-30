import sys
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

def run():
	lidar = RPLidar(PORT_NAME)
	outfile = open('lidardata.txt', 'w')
	try:
                print('Recording measurments... Press Crl+C to stop.')
		for measurment in lidar.iter_measurments():
			line = '\t'.join(str(v) for v in measurment)
			outfile.write(line + '\n')
	except KeyboardInterrupt:
		print('Stopping')
	lidar.stop()
	lidar.disconnect()
	outfile.close()

if __name__ == '__main__':
	run()
