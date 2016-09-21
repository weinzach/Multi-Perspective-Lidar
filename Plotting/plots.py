import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pointRotation import *
from lidarRead import *
import time
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

f = 'lidardata_7_1_16.txt'

data = lidarRead(f)
pointCloud = processScan(data)

xs = []
ys = []
zs = []

for scan in range(len(pointCloud)):
    init = initialRotation(pointCloud[scan])
    initialOffset(pointCloud[scan])
    turn = rotateCloud(init, [0,0,0], [0,0,1], np.radians(scan*1.8))
    x,y,z = acquirePoints(turn)
    xs.append(x)
    ys.append(y)
    zs.append(z)

x_agg = []
y_agg = []
z_agg = []
for scan in range(len(xs)):
    x_agg += xs[scan]
    y_agg += ys[scan]
    z_agg += zs[scan]

ax.scatter(x_agg,y_agg,z_agg)
plt.show()
 

