#!/usr/bin/python
# -*- coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage


"""
Contient deux fonctions qui calculent le spectre selon r=sqrt(p**2+q**2) et l'orientation teta.
a partir d'une image.
Les lignes mises en commentaire permettent de tracer les graphes spectra=f(r ou teta)
"""

def Rspectra(image):
	imNorm = image-np.mean(np.mean(image))
	[length, width]=imNorm.shape
	Ipq=length*width*(np.absolute(np.fft.fftshift(np.fft.fft2(imNorm)))**2)

	CentralPoint=[Ipq.shape[0]/2,Ipq.shape[1]/2]
	r=[]
	sigma=ndimage.variance(imNorm)
	for i in range(int(np.around(Ipq.shape[0]/2*np.sqrt(2)))+1):
		r.append([0,0])
	for i in range(Ipq.shape[0]):
		for j in range(Ipq.shape[1]/2+1):
			di=i-CentralPoint[0]
			dj=CentralPoint[1]-j
			dist=int(np.sqrt(di**2+dj**2))
			r[dist]=[r[dist][0]+1, r[dist][1]+(Ipq[i,j])]

	radialSpectrum=[]
	for i in range(len(r)):
		if r[i][0]!=0 :
			radialSpectrum.append(r[i][1]/r[i][0])
		else:
			radialSpectrum.append(0)

	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.plot(range(len(radialSpectrum)), (radialSpectrum))
	# plt.xlabel("r")
	# plt.ylabel("rSpectrum")
	# plt.show()
	# exit()
	return radialSpectrum

def TetaSpectra(image):
	imNorm = image-np.mean(np.mean(image))
	[length, width]=imNorm.shape
	Ipq=length*width*(np.absolute(np.fft.fftshift(np.fft.fft2(imNorm)))**2)

	CentralPoint=[Ipq.shape[0]/2,Ipq.shape[1]/2]
	a=[]
	sigma=ndimage.variance(imNorm)
	for i in range(0,180,1):
		a.append([0,0])

	for i in range(Ipq.shape[0]):
		for j in range(Ipq.shape[1]/2+1):
			di=i-CentralPoint[0]
			dj=CentralPoint[1]-j
			if dj==0 :
				teta=0
			else :
				tmp=2*np.arctan(dj/(di+np.sqrt(di**2+dj**2)))
				teta=int(np.degrees(tmp))
			a[teta]=[a[teta][0]+1, a[teta][1]+Ipq[i,j]]

	angularSpectrum=[]
	for i in range(len(a)):
		if a[i][0]!=0 :
			angularSpectrum.append(a[i][1]/a[i][0])
		else:
			angularSpectrum.append(0)

	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.plot(range(len(angularSpectrum)), (angularSpectrum))
	# plt.xlabel("Teta")
	# plt.ylabel("Angular Spectrum")
	# plt.show()

	return angularSpectrum/sigma**2
