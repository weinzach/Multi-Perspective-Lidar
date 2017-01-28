import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN

ANGLE_INDEX = 2
RADIUS_INDEX = 3
STEP_INDEX = 4

DEGREES_PER_STEP = 360.0 / 389.47

INCLINATION_ANGLE = 30.0

IMPORT_FILE = "lidar_3d.npz"

class Plotter3D():
	def __init__(self, filename, N=0):
		# Read in raw data from file
        # Stop at the end of the file, or when N entries have been read
		data = np.load(filename)

		# Create a place holder for out rectangular 3D data
		self.Xs = data['x']
		self.Ys = data['y']
		self.Zs = data['z']

	def plot(self, stride=10):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(self.Xs[::stride], self.Ys[::stride], self.Zs[::stride])
		plt.show()

	def cluster(self, epsilon, points):
		data = np.zeros((len(self.Xs),3))
		for element in range(len(self.Xs)):
			data[element,0]=self.Xs[element]
			data[element,1]=self.Ys[element]
			data[element,2]=self.Zs[element]

		fig = plt.figure()

		ax = fig.add_subplot(1,2,1, projection='3d')
		ax.scatter(data[:,0],data[:,1],data[:,2], s=4,marker='+')

		db = DBSCAN(eps=epsilon, min_samples = points).fit(data)
		labels = db.labels_
		core_samples_mask = np.zeros_like(labels, dtype=bool)
		core_samples_mask[db.core_sample_indices_] = True
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

		unique_labels = set(labels)
		colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
		ax=fig.add_subplot(1,2,2,projection='3d')
		for k, col in zip(unique_labels, colors):
		    if k == -1:
		        # Black used for noise.
		        col = 'k'

		    class_member_mask = (labels == k)

		    xyz = data[class_member_mask & core_samples_mask]
		    if len(xyz) > 3:
		   		#ax.plot_wireframe(xyz[:,0],xyz[:,1],xyz[:,2])
		   		ax.plot(xyz[:,0],xyz[:,1],xyz[:,2], 'o', markerfacecolor=col, markeredgecolor='k', markersize=4)

		plt.show()



if __name__ == '__main__':
	dr = Plotter3D(IMPORT_FILE)
	dr.cluster(100, 5)
	#dr.plot(10)
