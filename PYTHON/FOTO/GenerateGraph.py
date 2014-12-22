#!/usr/bin/python
# -*- coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as image
from PIL import Image 


def GenerateRspectra(radialS, data, idx, res):
	color=['r','b','g','c','m','y','b','w']
	fig = plt.figure()
	ax = fig.add_subplot(111)
	max=0
	for i in range(res.shape[0]):
	    centralsPoints = distances(data, res[i], idx, i)
	    plt.plot(range(len(radialS[centralsPoints])), (radialS[centralsPoints]), label='R-spectra du point le plus central de chaque classe '+str(i), color=color[i])
	    if max<np.max(radialS[centralsPoints]):
			max=np.max(radialS[centralsPoints])
	plt.xlabel("r")
	plt.ylabel("Spectre radial du point le plus central de la classe")
	plt.legend()
	plt.ylim((0, max))
	plt.savefig('RspectraCentralPointInEachClass.png')

	plt.axis
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for i in range(res.shape[0]):
		sumRSpectra=np.zeros((len(radialS[0])))
		for j in np.where(idx==i)[0]:
			sumRSpectra+=radialS[j]
		mean=sumRSpectra/len(np.where(idx==i)[0])
		plt.plot(range(len(mean)), mean,label='R-spectra moyen de chaque classe '+str(i), color=color[i])
	plt.xlabel("r")
	plt.ylabel("Moyenne des spectres par classes")
	plt.legend()
	plt.ylim((0, max))
	plt.savefig('MeanRspectraInEachClass.png')

def WriteRspectraImages(radialSpectra):

	[length, width, dim]=radialSpectra.shape
	rgbArray = np.zeros((length,width), 'uint8')
	radialSpectraLog=np.log(radialSpectra)
	radialSpectraLog[np.isneginf(radialSpectraLog)] = 0
	radialSpectraLog100=np.around(radialSpectraLog, decimals=3)
	minVal=0
	maxVal=np.max(np.max(np.max(radialSpectraLog100)))
	dynamic = maxVal-minVal
	# print()
	radialSnorm=((radialSpectraLog100-minVal)/dynamic)*255

	

	for r in range(dim):
		for i in range(length):
			for j in range(width):
				rgbArray[i,j]=radialSnorm[i][j][r]
		img = Image.fromarray(rgbArray)
		img.save('radialSpectrumNumber'+str(r)+'.png')


def GenerateIntertieACP(inertie):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.bar(range(len(inertie)), inertie*100, color='r')
	plt.xlabel('ACP axis')
	plt.ylabel('Variance expliquee par ACP en %')
	plt.savefig('IntertieACP.png')

def GenerateACPax1ax2KmeansClasses(data,idx):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	color=['r.','b.','g.','c.','m.','y.','b.','w.']
	for i in range(len(data)):
		my_cmap=color[idx[i]]
		plt.plot(data.T[0][i],data.T[1][i],  my_cmap)
	plt.xlabel('Axe 1 ACP')
	plt.ylabel('Axe 2 ACP')
	# ax.set_xlim((-8,8))
	# ax.set_ylim((-4,4))
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')
	plt.savefig('GenerateACPax1ax2KmeansClasses.png')
	# plt.show()

def distances(data, xy, idx, k):
	dMin=10000
	iMin=0
	for i in range(len(data)):
		if idx[i]==k:
			d0 = (data[i][0]-xy[0])**2
			d1 = (data[i][1]-xy[1])**2
			d=np.sqrt(d0+d1)
			if d<dMin: dMin=d; iMin=i
	return iMin

def GenerateACPax1ax2TextureImage(data, idx, res, imagette, nb_classes):
	dpi = 72; imageSize = imagette[0].shape

	fig = plt.figure(dpi=dpi)
	ax = fig.add_subplot(111)
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')

	line, = ax.plot(res.T[0],res.T[1],"bo",markersize=imageSize[0] * (dpi/ 96))
	fig.patch.set_alpha(0)
	line._transform_path()
	path, affine = line._transformed_path.get_transformed_points_and_affine()
	path = affine.transform_path(path)

	for i in range(nb_classes):
	    px=path.vertices[i][0]-((imageSize[0])/2)
	    py=path.vertices[i][1]-((imageSize[1])/2)

	    centralsPoints = distances(data, res[i], idx, i)

	    fig.figimage(imagette[centralsPoints], px, py,origin="upper", cmap=plt.gray())
	plt.xlabel('Axe 1 ACP')
	plt.ylabel('Axe 2 ACP')
	plt.savefig('GenerateACPax1ax2TextureImage.png')
	# plt.show()

def GenerateClassif(image, WindowsSize, idx, data,pas):
	[length, width]=image.shape
	rgbArray = np.zeros((length,width,3), 'uint8')
	k=0
	colors=np.array([[1,104,139],[46,139, 87],[139,58,98], [255,127,36], [127,255,0], [0,250,154] ])
	colors=(colors/float(255))

	for i in range( WindowsSize/2, length - WindowsSize/2, pas):
		for j in range( WindowsSize/2, width - WindowsSize/2 +1 , pas):
			
			classe=idx[k]
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,0]=(colors[classe][0]*image[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1]).astype(int)
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,1]=(colors[classe][1]*image[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1]).astype(int)
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,2]=(colors[classe][2]*image[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1]).astype(int)
			k+=1
	img = Image.fromarray(rgbArray)
	img.save('classif.png')
	img.show()

def GenerateACPImage(projectedValues, image, WindowsSize,pas):
	[length, width]=image.shape
	rgbArray = np.zeros((length,width,3), 'uint8')

	data=np.array(projectedValues[0:3])
	dataNorm=[]
	for i in range(3):

		minVal = np.min(data[i])

		dataPos=data[i] + abs(minVal)
		minVal = np.min(dataPos)
		maxVal = np.max(dataPos)
		dynamic = maxVal-minVal
		a=(dataPos/dynamic*255)
		dataNorm.append(a.astype(int))
	k=0


	for i in range( WindowsSize/2, length - WindowsSize/2, pas):
		for j in range( WindowsSize/2, width - WindowsSize/2 +1 , pas):
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,0]=dataNorm[0][k]*np.ones((pas,pas))
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,1]=dataNorm[1][k]*np.ones((pas,pas))
			rgbArray[i-pas/2 : i + pas/2 +1, j-pas/2 : j+pas/2 + 1,2]=dataNorm[1][k]*np.ones((pas,pas))
			k+=1
	img = Image.fromarray(rgbArray)

	img.show()
	img.save('ACPImage.png')
