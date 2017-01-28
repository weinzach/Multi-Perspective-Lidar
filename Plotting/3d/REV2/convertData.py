import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN

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

	def calculate(self, stride=1):
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

		print("Exporting to Files...")

		np.savez('./'+EXPORT_FILE1, x=self.Xs, y=self.Ys,z=self.Zs)
		np.savetxt('./'+EXPORT_FILE2, np.c_[self.Xs,self.Ys,self.Zs])

		print("Done! Files saved to "+EXPORT_FILE1+ " and "+EXPORT_FILE2)


if __name__ == '__main__':
	dr = DataConversion('lidardata.txt')
	dr.calculate(stride=10)
