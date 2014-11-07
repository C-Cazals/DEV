#!/usr/bin/python
 
# Adapted from http://hackmap.blogspot.com/2007/09/k-means-clustering-in-scipy.html
 
import numpy as np
import matplotlib 
matplotlib.use('Agg')
from scipy.cluster.vq import *
import pylab
pylab.close()
 
# generate 3 sets of normally distributed points around
# different means with different variances
# pt1 = np.random.normal(1, 0.2, (100,2))
# pt2 = np.random.normal(2, 0.5, (300,2))
# pt3 = np.random.normal(3, 0.3, (100,2))
x=[2,1,3,2,1,3, 8,9,8,9,7]
y=[5,4,6,4,5,4, 1,2,3,1,2]
data=np.array([x,y]).T
print data.shape
print data

# # slightly move sets 2 and 3 (for a prettier output)
# pt2[:,0] += 1
# pt3[:,0] -= 0.5
 
# xy = np.concatenate((pt1, pt2, pt3))
 
# kmeans for 3 clusters

print res  
print idx
colors = ([([0.4,1,0.4],[1,0.4,0.4])[i] for i in idx])
 
# plot colored points
pylab.scatter(data[:,0],data[:,1], c=colors)
 
# mark centroids as (X)
pylab.scatter(res[:,0],res[:,1], marker='o', s = 500, linewidths=2, c='none')
pylab.scatter(res[:,0],res[:,1], marker='x', s = 500, linewidths=2)
# matplotlib.pyplot.show()
pylab.savefig('kmeans.png')


