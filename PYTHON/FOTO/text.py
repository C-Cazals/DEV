#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt
import csv
import scipy.spatial.distance as dist
import scipy.cluster.vq as cluster



ifile  = open('data.csv', "rb")
reader = csv.reader(ifile, delimiter='\t')
data=[]
b=[]
# c=[]
for row in reader:
	b.append(np.array(row).astype(float))
	data=np.array(b)

ifile.close()

distanceMatrix=dist.pdist(data)

linkageMatrix=hac.linkage(distanceMatrix)	


hac.dendrogram(linkageMatrix)
# fcluster(Z, t[, criterion, depth, R, monocrit])	Forms flat clusters from the hierarchical clustering defined by the linkage matrix Z.
# fclusterdata(X, t[, criterion, metric, ...])	Cluster observation data using a given metric.
# leaders(Z, T)	Returns the root nodes in a hierarchical clustering.
# These are routines for agglomerative clustering.
print(linkageMatrix)
exit()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(data[:,0], data[:,1], 'k.')

plt.show()


exit()

  