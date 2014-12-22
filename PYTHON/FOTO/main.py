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
import os


import GenerateGraph

if (len(sys.argv) != 5) :
	print("Usage : ", sys.argv[0], "imageFile.tif", "WindowsSize", "Nombre de classes", "pas de glissement de la fenetre")
	exit()



imageFile=sys.argv[1]
WindowsSize=int(sys.argv[2])
nb_classes=int(sys.argv[3])
image = np.array(Image.open(imageFile))
[length, width]=image.shape

pas=int(sys.argv[4])
if pas%2==0:
	pas+=1
print("WindowsSize : ", WindowsSize)
radialS=[]
imagette=[]

iList=range( WindowsSize/2, length - WindowsSize/2 +1, pas)
jList=range( WindowsSize/2, width - WindowsSize/2 +1 , pas)
radialSpectra=np.zeros((iList[-1]/pas+1, jList[-1]/pas+1, WindowsSize/2*np.sqrt(2)+1))
r=np.zeros((jList[-1]/pas+1, WindowsSize/2*np.sqrt(2)+1))
print( radialSpectra.shape)
print( r.shape)
for i in iList:
	sys.stdout.write('\r' + "Computing Rspectra .... " + str(int((i/float(length+1))*100)) + "%")
	sys.stdout.flush()
	for j in jList:
		im = image[ i-WindowsSize/2 : i + WindowsSize/2 +1, j-WindowsSize/2 : j+WindowsSize/2 + 1]
		r[j/pas,:]=ComputeRspectra.Rspectra(im)
	np.savetxt('radialSpectraLine'+str(i/pas)+'.txt', r)
print("")
		

for i in iList :
	radialSpectra[i/pas]=np.loadtxt('radialSpectraLine'+str(i/pas)+'.txt')
	os.remove('radialSpectraLine'+str(i/pas)+'.txt')

GenerateGraph.WriteRspectraImages(radialSpectra)


exit('FIN')

























radialS_stand=[]
for i in radialS:
	if np.std(i)!=0:
		radialS_stand.append((i-np.mean(i))/np.std(i))
	for j in i:
		if (np.isfinite(j)==0):
			print(j)

print("Writing R-spectra Images...")

print("Computing PCA...")
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

print("Generating graphs...")
GenerateGraph.GenerateRspectra(radialS, data, idx, res)

GenerateGraph.GenerateIntertieACP(pca.fracs)

GenerateGraph.GenerateACPax1ax2KmeansClasses(data, idx)

GenerateGraph.GenerateACPax1ax2TextureImage(data, idx, res, imagette, nb_classes)

print("Generating classification...")
GenerateGraph.GenerateClassif(image, WindowsSize, idx, data, pas)

print("Generating PCA Image....")
GenerateGraph.GenerateACPImage(projectedValues, image, WindowsSize, pas)

exit("Process completed.")