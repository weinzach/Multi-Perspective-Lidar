import socketio
import eventlet.wsgi
from flask import Flask, render_template
import matplotlib.pyplot as plt
import numpy as np

sio = socketio.Server()
app = Flask(__name__)

DMAX = 6000
IMIN = 0
IMAX = 50

plt.ion()
subplot = plt.subplot(111, projection='polar')
plot = subplot.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX], cmap=plt.cm.Greys_r, lw=0)
subplot.set_rmax(DMAX)
subplot.grid(True)
plt.show()

def update(plot, scan):
    '''Updates plot'''
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    plot.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    plot.set_array(intens)
    plt.show()
    plt.pause(0.001)

@sio.on('connect', namespace='/chat')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('message', namespace='/')
def message(sid, data):
    update(plot, data)

@sio.on('disconnect', namespace='/chat')
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)