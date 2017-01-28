from sklearn.cluster import DBSCAN
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
