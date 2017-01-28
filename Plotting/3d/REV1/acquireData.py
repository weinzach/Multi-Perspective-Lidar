from lidarRead import lidarRead
import numpy as np
import time
fig = plt.figure()
ax1 = fig.add_subplot(111)

i = 0

file = 'lidardata_7_1_16.txt'


data = lidarRead(file)
rs = []
thetas = []
xs = []
ys = []
for scan in range(len(data)):
    r = []
    theta = []
    x = []
    y = []
    for point in range(len(data[scan])):
        thval = np.radians(float(data[scan][point][0]))
        rval = float(data[scan][point][1])
        if rval > 2000:
            x.append(np.cos(thval)*rval)
            y.append(np.sin(thval)*rval)
        
        
        '''
        if float(data[scan][point][1]) > 5000:
            rval = float(data[scan][point][1])
        else:
            rval = 6000
        thval = np.radians(float(data[scan][point][0]))   
        theta.append(thval)
        x.append(np.cos(thval)*rval)
        y.append(np.sin(thval)*rval)
        '''
    rs.append([r])
    thetas.append([theta])
    xs.append([x])
    ys.append([y])
