#!/usr/bin/python
# -*- coding: utf-8

from __future__ import print_function
import sys
import numpy as np
from PIL import Image 
import csv
import ComputeRspectra
from matplotlib.mlab import PCA
import scipy.cluster.vq as cluster


import GenerateGraph

if (len(sys.argv) != 4) :
	print("Usage : ", sys.argv[0], "imageFile.tif", "WindowsSize", "Nombre de classes")
	exit()




imageFile=sys.argv[1]
WindowsSize=int(sys.argv[2])
nb_classes=int(sys.argv[3])
image = np.array(Image.open(imageFile))
[length, width]=image.shape

pas=1
if pas%2==0:
	pas+=1
print("WindowsSize : ", WindowsSize)
radialS=[]
imagette=[]

for i in range( WindowsSize/2, length - WindowsSize/2, pas):
	# print( i)
	sys.stdout.write('\r' + "Computing Rspectra .... " + str(int((i/float(length+1))*100)) + "%")
	sys.stdout.flush()
	for j in range( WindowsSize/2, width - WindowsSize/2 +1 , pas):
		im = image[ i-WindowsSize/2 : i + WindowsSize/2 +1, j-WindowsSize/2 : j+WindowsSize/2 + 1]
		# print(im.shape)
		r=ComputeRspectra.Rspectra(im)
		imagette.append(im)
		radialS.append(r)


print("")

# print(np.array(radialS).shape)

radialS_stand=[]
for i in radialS:
	if np.std(i)!=0:
		radialS_stand.append((i-np.mean(i))/np.std(i))
	for j in i:
		if (np.isfinite(j)==0):
			print(j)


GenerateGraph.WriteRspectraImages(radialS, image, WindowsSize, pas)
exit()

pca=PCA(np.array(radialS_stand))
projectedValues=pca.Y.T

data=np.array(projectedValues[0:2].T)


ofile  = open('data.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)

for row in data:
    writer.writerow(row)


ofile.close()
res, idx = cluster.kmeans2(data,nb_classes)

while (len(res)!=nb_classes):
	print('Running K-means again')
	res, idx = kmeans2(data,nb_classes)

GenerateGraph.GenerateRspectra(radialS, data, idx, res)

GenerateGraph.GenerateIntertieACP(pca.fracs)

GenerateGraph.GenerateACPax1ax2KmeansClasses(data, idx)

GenerateGraph.GenerateACPax1ax2TextureImage(data, idx, res, imagette, nb_classes)

GenerateGraph.GenerateClassif(image, WindowsSize, idx, data, pas)

GenerateGraph.GenerateACPImage(projectedValues, image, WindowsSize, pas)

exit("OK")