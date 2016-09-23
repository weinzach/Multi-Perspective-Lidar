import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN

ANGLE_INDEX = 2
RADIUS_INDEX = 3
STEP_INDEX = 4

DEGREES_PER_STEP = 360.0 / 389.47

INCLINATION_ANGLE = 30.0

class DataRenderer():
	def __init__(self, filename, N=0):
		# Read in raw data from file
        # Stop at the end of the file, or when N entries have been read
		self.raw_data =[]
		with open(filename, 'r') as f:
			for n, line in enumerate(f):
				if N != 0 and n >= N:
					break
				words = line.split()
				self.raw_data.append( [float(words[ANGLE_INDEX]), float(words[RADIUS_INDEX]), int(words[STEP_INDEX])] )
			else:
				print('Reached end of file')

		# Create a place holder for out rectangular 3D data
		self.Xs = []
		self.Ys = []
		self.Zs = []

	def calculate(self, stride=1):
		# Reset
		self.Xs = []
		self.Ys = []
		self.Zs = []

		# Calculate
		for angle1, radius, stepNum in self.raw_data[::stride]:
			# Get this raw data point into a more useful form
			angle2 = stepNum * DEGREES_PER_STEP
			theta1 = angle1 * np.pi / 180.0
			theta2 = angle2 * np.pi / 180.0
			thetaInc = INCLINATION_ANGLE * np.pi / 180.0
			ref = np.matrix( [[1.0, 0.0, 0.0]] ).transpose()

			# Rotate about the z-axis by theta1
			ref = np.matrix([[ np.cos(theta1), np.sin(theta1), 0],
							 [-np.sin(theta1), np.cos(theta1), 0],
							 [ 0             , 0             , 1]]) * ref

			# Rotate about the y-axis by thetaInc
			ref = np.matrix([[ np.cos(thetaInc), 0, np.sin(thetaInc)],
							 [ 0,                1,                0],
							 [-np.sin(thetaInc), 0, np.cos(thetaInc)]]) * ref

			# Rotate about the z-axis by theta2
			ref = np.matrix([[ np.cos(theta2), np.sin(theta2), 0],
							 [-np.sin(theta2), np.cos(theta2), 0],
							 [ 0             , 0             , 1]]) * ref

			# Multiply by radius and record
			point_mat = radius * ref

			self.Xs.append(point_mat[0,0])
			self.Ys.append(point_mat[1,0])
			self.Zs.append(point_mat[2,0])

	def plot(self, stride=1):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		ax.scatter(self.Xs[::stride], self.Ys[::stride], self.Zs[::stride])
		fig.show()

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
	dr = DataRenderer('lidardata.txt')
	dr.calculate(stride=10)
	dr.cluster(100, 5)
	#dr.plot(100, 5)
	#input()
