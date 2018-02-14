# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = 'threading'

import socketio
import time
from flask import Flask, render_template
from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
DMAX = 6000
IMIN = 0
IMAX = 50

sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
thread = None

def background_thread():
    while True:
        '''Main function'''
        lidar = RPLidar(PORT_NAME)
        for scan in lidar.iter_scans():
            sio.emit('message', {'data': scan},
                       namespace='/')
        lidar.stop()
        lidar.disconnect()

@app.route('/')
def index():
    return 'Server is Working'

@sio.on('disconnect request', namespace='/')
def disconnect_request(sid):
    sio.disconnect(sid, namespace='/')


@sio.on('connect', namespace='/')
def test_connect(sid, environ):
    print('Client connected')

@sio.on('disconnect', namespace='/')
def test_disconnect(sid):
    print('Client disconnected')


if __name__ == '__main__':
    if sio.async_mode == 'threading':
        # deploy with Werkzeug
        if thread is None:
            thread = sio.start_background_task(background_thread)
        app.run(host='0.0.0.0', port=8000,threaded=True)
    else:
        print('Unknown async_mode: ' + sio.async_mode)
