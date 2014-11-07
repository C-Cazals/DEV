#!/usr/bin/python
# -*- coding: utf-8

#
# Example boxplot code
#
import matplotlib as mpl
import matplotlib.pyplot as plt 
import random
import csv
import sys
import numpy as np
import array


print len(sys.argv)
if (len(sys.argv) != 2) :
	print "Usage : ", sys.argv[0], "csvFile"
	exit()

print("DEBUT")


reader=csv.reader(open(sys.argv[1],"rb"),delimiter=',')
next(reader, None)
x=list(reader)
result=np.array(x).astype('float')
# print result.shape
# exit("FIN")
# nbClasses=result.shape[1]-3
# for i in range(nbClasses):

HH1=[]
HH2=[]
HH3=[]

VV1=[]
VV2=[]
VV3=[]

HH4=[]
VV4=[]
# for rows in range(result.shape[0]):
# 	if result[rows,1]==0 :
# 		zone1.append(10*np.log10(result[rows,3]))
# 	if result[rows,1]==1 :
# 		zone2.append(10*np.log10(result[rows,3]))
# 	if result[rows,1]==2 :
# 		zone3.append(10*np.log10(result[rows,3]))
tab=[]
for i in range(50000):
	tab.append(random.randint(0, result.shape[0]))

for rows in tab:
	if result[rows,5]==1 :
		HH1.append(10*np.log10(result[rows,3]))
		VV1.append(10*np.log10(result[rows,4]))
	if result[rows,5]==2 :
		HH2.append(10*np.log10(result[rows,3]))
		VV2.append(10*np.log10(result[rows,4]))
	if result[rows,5]==3 :
		HH3.append(10*np.log10(result[rows,3]))
		VV3.append(10*np.log10(result[rows,4]))
	if result[rows,5]==4 :
		HH4.append(10*np.log10(result[rows,3]))
		VV4.append(10*np.log10(result[rows,4]))



fig = plt.figure()
ax1 = fig.add_subplot(111)
# plt.xlim([-30, 5])
# plt.ylim([-30, 5])
ax1.plot(HH1, VV1, 'b.', markersize=1, label='the data')
ax1.plot(HH2, VV2, 'r.', markersize=1, label='the data')
ax1.plot(HH3, VV3, 'g.', markersize=1, label='the data')
ax1.plot(HH4, VV4, 'y.', markersize=1, label='the data')

plt.show()

exit("FIN")