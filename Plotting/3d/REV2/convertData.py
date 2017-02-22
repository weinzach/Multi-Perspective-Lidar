import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
import random

ANGLE_INDEX = 2
RADIUS_INDEX = 3
STEP_INDEX = 4

DEGREES_PER_STEP = 360.0 / 389.47

INCLINATION_ANGLE = 30.0

EXPORT_FILE1 = "lidar_3d.npz"
EXPORT_FILE2 = "lidar_3d.txt"

class DataConversion():
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

	def calculate(self, stride=1, clustering=False):
		print("Converting to 3D Point Array...")

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
		if(clustering==True):
	   		self.cluster(100, 5)
		else:
			print("Exporting to Files...")
			np.savez('./'+"NC_"+EXPORT_FILE1, x=self.Xs, y=self.Ys,z=self.Zs)
			np.savetxt('./'+"NC_"+EXPORT_FILE2, np.c_[self.Xs,self.Ys,self.Zs])
			print("Done! Files saved to NC_"+EXPORT_FILE1+ " and NC_"+EXPORT_FILE2)


	def cluster(self, epsilon, points):

		data = np.zeros((len(self.Xs),3))
		for element in range(len(self.Xs)):
			data[element,0]=self.Xs[element]
			data[element,1]=self.Ys[element]
			data[element,2]=self.Zs[element]

		db = DBSCAN(eps=epsilon, min_samples = points).fit(data)
		core_samples = db.core_sample_indices_
		labels = db.labels_
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

		print(str(n_clusters_)+" clusters found!")

		#Array to Store Each Cluster
		clusterData = []
		colors = ["RED","GREEN","BLUE","YELLOW","MAGENTA"]
		clusterColor = []

		#Append Found Clusters to Array (Using Random Colors)
		for i in xrange(n_clusters_):
			clusters = [data[labels == i]]
			clusterData.append(clusters)
			clusterColor.append(random.choice(colors))

		#Export Array Wiht Colors
		print("Exporting to File...")
		f1=open(" C_"+EXPORT_FILE2, 'w+')
		for i in range(0,len(clusterData)):
			for cPoints in clusterData[i][0]:
				cPoints = cPoints.tolist()
				cPoints.append(clusterColor[i])
				cPoints.append(i)
				f1.write(" ".join(map(lambda x: str(x), cPoints)) + "\n")

		#Close File
		f1.close
		print("Done! Files saved to C_"+EXPORT_FILE2)


if __name__ == '__main__':
	dr = DataConversion('lidardata.txt')
	dr.calculate(stride=10, clustering=True)
