# It must use dbscan and then save each cluster as a new file
# Write in program to see the text file 
print(__doc__)

import numpy as np 

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import read_scans as rs
#######################################################
#Generate sample data 
centers = [[1,1,1],[-1,-1,1],[1,-1,-1]]

X, labels_true = make_blobs(n_samples = 750, centers = centers, cluster_std = 0.4, random_state = 0)
f = 'Testfile.txt'
X = rs.read_scans(f)
X = rs.filter_scans(X)
########################################################################
#Plot sample data
fig = plt.figure()
ax = fig.add_subplot(1,2,1, projection='3d')

ax.scatter(X[:,0], X[:,1],X[:,2])


########################################################################
#Compute DBSCAN

db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True 
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)

#######################################################################
#Plot result
ax = fig.add_subplot(1,2,2, projection='3d')
unique_labels = set(labels)

colors = plt.cm.Spectral(np.linspace(0,1,len(unique_labels)))
for k, col in zip(unique_labels, colors):
	if k == -1:
		col = 'k'

	class_member_mask = (labels == k)

	xyz = X[class_member_mask & core_samples_mask]
	
	ax.plot(xyz[:,0],xyz[:,1],xyz[:,2], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)

	#xyz = X[class_member_mask & ~core_samples_mask]
	#ax.plot(xyz[:,0],xyz[:,1],xyz[:,2], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

plt.show()

def cluster(data, epsilon, points):
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
	write("LukesSwiggitySw4g.txt")

