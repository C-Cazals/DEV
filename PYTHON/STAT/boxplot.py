#!/usr/bin/python

#
# Example boxplot code
#
import matplotlib as mpl
import matplotlib.pyplot as plt 
import csv
import sys
import numpy as np


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
zone1=[]
zone2=[]
zone3=[]
zone4=[]
for rows in range(result.shape[0]):
	if result[rows,1]==1 :
		zone1.append(10*np.log10(result[rows,4]))
	if result[rows,1]==2 :
		zone2.append(10*np.log10(result[rows,4]))
	if result[rows,1]==3 :
		zone3.append(10*np.log10(result[rows,4]))
	if result[rows,1]==4 :
		zone4.append(10*np.log10(result[rows,4]))
# for rows in range(result.shape[0]):
# 	if result[rows,5]==1 :
# 		zone1.append(result[rows,4])
# 	if result[rows,5]==2 :
# 		zone2.append(result[rows,4])
# 	if result[rows,5]==3 :
# 		zone3.append(result[rows,4])
# 	if result[rows,5]==4 :
# 		zone4.append(result[rows,4])

# plt.xlim([-30, 5])
# plt.ylim([-30, 5])

data = [zone1, zone2, zone3, zone4]
fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot(data)
ax.set_xticklabels(['Ble', 'Chene', 'Mais', 'Praire Temp'])
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


plt.show()
exit("FIN")