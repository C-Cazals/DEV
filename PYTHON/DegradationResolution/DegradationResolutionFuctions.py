#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import cmath
import DegradationResolutionFuctions as DRF

def square(mat):
  squareMat=np.zeros((mat.shape))
  for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
      squareMat[i,j]=mat[i,j]**2
  return squareMat
          
def Stretch(image):
  minI=np.min(np.min(image))
  # print(minI)
  if(minI<0):
    # print(image)
    image=image+np.absolute(minI)
    # print(image)
    # exit()
    minI=0
  else:
    minI=np.min(np.min(image))
  dynamic=np.max(np.max((image)) - minI)
  # print(np.max(np.max((image))), minI)
  # print(dynamic)

  mean = np.mean(np.mean((image)))
  # print(mean)
  imageStretched=(np.absolute(dynamic-(image))/mean)*10
  # imageStretched=(np.absolute(dynamic-(image))/mean)*255
  # print(np.absolute(dynamic-image)/mean)
  # exit()
  # print(imageStretched)
  return imageStretched

def ComputeMeanLineSpectra(img):
  [width, length]=img.shape
  MeanLine=np.zeros((length))
  for l in range(width):
    MeanLine+=np.absolute(img[l,:])
  MeanLine=MeanLine/width
  return(MeanLine) 


def ComputeMeanColumnSpectra(img):
  [width, length]=img.shape
  MeanColumn=np.zeros((width))
  for c in range(length):
    MeanColumn+=np.absolute(img[:,c])
  MeanColumn=MeanColumn/length
  return(MeanColumn)


def CutLineSpectra(img, MeanLineSpectra, rangeRatio):
   [width, length]=img.shape
   if(rangeRatio==1):
      return(img)
   rangeCut=np.around(length/2-length*rangeRatio/(2))
   imgLineDegraded=np.zeros((img.shape), dtype=complex)
   for l in range(width):

      line=img[l,:]/MeanLineSpectra
      # # Coupe aux extremintés du spectre
      # rangeCut=length*rangeRatio/(2)
      # imgLineDegraded[l][0:rangeCut] = line[0:rangeCut]
      # imgLineDegraded[l][-rangeCut:]=line[-rangeCut:]

      # Coupe au milieu du spectre
      # print(line[rangeCut:-rangeCut].shape)
      # print(line.shape)
      # print(rangeCut)
      imgLineDegraded[l][rangeCut:-rangeCut]=line[rangeCut:-rangeCut]
      # exit()
      # fig = plt.figure()
      # ax = fig.add_subplot(111)
      # ax.plot(range(length), np.absolute(MeanLineSpectra), 'g')
      # ax.plot(range(length), np.absolute(img[l,:]), 'y')
      # plt.show()
      # exit()

   #Multiplication par le spectre moyen
   MeanLineSpectraResampled=np.zeros((MeanLineSpectra.shape))
   print(rangeCut)
   # print(MeanLineSpectraResampled[rangeCut:-rangeCut].shape, resample(MeanLineSpectra,length-2*rangeCut+2).shape)
   MeanLineSpectraResampled[rangeCut:-rangeCut]=resample(MeanLineSpectra,length-2*rangeCut)
   # MeanLineSpectraResampled=np.concatenate((zero.T, tmp.T, zero.T))
   for l in range(width):
      imgLineDegraded[l]=imgLineDegraded[l]*MeanLineSpectraResampled
   
   # fig = plt.figure()
   # ax = fig.add_subplot(111)
   # ax.plot(range(length), np.absolute(MeanLineSpectra), 'g')
   # ax.plot(range(length), np.absolute(MeanLineSpectraResampled), 'y')
   # plt.show()
   # exit()

   return(imgLineDegraded)








def CutColumnSpectra(img, MeanColumnSpectra, azimutRatio):
   [width, length]=img.shape
   if(azimutRatio==1):
      return(img)
   azimutCut=np.around(width/2-width*azimutRatio/(2))
   imgColumnDegraded=np.zeros((img.shape), dtype=complex)
   for c in range(length):
      col=img[:,c].T/MeanColumnSpectra

      # print(img[:,c])
      # print(MeanColumnSpectra)
      # # prin
      # print(img[:,c].shape)
      # print(MeanColumnSpectra.shape)
      # print(col.shape)
      # # Coupe aux extremintés du spectre
      # azimutCut=width*azimutRatio/(2)
      # imgColumnDegraded[l][0:azimutCut] = col[0:azimutCut]
      # imgColumnDegraded[l][-azimutCut:]=col[-azimutCut:]

      # Coupe au milieu du spectre
      # print( imgColumnDegraded[:,c][azimutCut:-azimutCut].shape, col[azimutCut:-azimutCut].shape)
      imgColumnDegraded[:,c][azimutCut:-azimutCut]=col[azimutCut:-azimutCut]

      # fig = plt.figure()
      # ax = fig.add_subplot(111)
      # ax.plot(range(width), np.absolute(MeanColumnSpectra), 'g')
      # ax.plot(range(width), np.absolute(img[l,:]), 'y')
      # plt.show()
      # exit()

  #Multiplication par le spectre moyen
   MeanColumnSpectraResampled=np.zeros((MeanColumnSpectra.shape))
   # print(azimutCut)
   # print(MeanColumnSpectraResampled[azimutCut:-azimutCut].shape, resample(MeanColumnSpectra,width-2*azimutCut).shape)
   MeanColumnSpectraResampled[azimutCut:-azimutCut]=resample(MeanColumnSpectra,width-2*azimutCut)
   # MeanColumnSpectraResampled=np.concatenate((zero.T, tmp.T, zero.T))
   for c in range(length):
      imgColumnDegraded[:,c]=imgColumnDegraded[:,c]*MeanColumnSpectraResampled
     
   # fig = plt.figure()
   # ax = fig.add_subplot(111)
   # ax.plot(range(width), np.absolute(MeanColumnSpectra), 'g')
   # ax.plot(range(width), np.absolute(MeanColumnSpectraResampled), 'y')
   # plt.show()
   # exit()


   return(imgColumnDegraded)


def MakeComplexImage(image1, image2):
   [width, length]=image1.shape
   complexImage=np.zeros((image1.shape), dtype=complex)
   for i in range(width):
      for j in range(length):
         complexImage[i,j]=cmath.rect(image1[i,j], image2[i,j])
   return complexImage

def UnMakeComplexImage(complexImage):
   [width, length]=complexImage.shape
   intensite=np.zeros((complexImage.shape))
   phase=np.zeros((complexImage.shape))
   for i in range(length):
      for j in range(width):
         [a,b]=cmath.polar(complexImage[i,j])
         intensite[i,j]=a
         phase[i,j]=b
   return [intensite, phase]
