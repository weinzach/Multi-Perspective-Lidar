'''Animates distances and measurment quality'''
from rplidar import RPLidar
from socketIO_client import SocketIO, LoggingNamespace

socketIO = SocketIO('192.168.1.116', 8000, LoggingNamespace)

PORT_NAME = '/dev/ttyUSB0'
DMAX = 6000
IMIN = 0
IMAX = 50

def run():
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    for scan in lidar.iter_scans():
	socketIO.emit('message',scan)
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()
