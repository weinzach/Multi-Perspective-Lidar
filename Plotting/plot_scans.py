import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import read_scans as rs 
import dbscan

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

f = 'lidardata.txt'

scans = rs.read_scans(f)

processed_scans = rs.filter_scans(scans)

xs = []
ys = []
zs = []

for scan in range(len(processed_scans)):
	for point in range(len(processed_scans[scan])):
		xs.append(processed_scans[scan][point][0])
		ys.append(processed_scans[scan][point][1])
		zs.append(processed_scans[scan][point][2])

data = np.zeros((len(xs),3))
for element in range(len(xs)):
	data[element,0]=xs[element]
	data[element,1]=ys[element]
	data[element,2]=zs[element]

processed_data = dbscan.cluster(data, 100, 5)
#ax.scatter(xs,ys,zs, s= 2, marker='+')

#plt.show()

