#!/usr/bin/python 
# -*- coding: utf-8 -*-


# Import the otb applications package 
import numpy as np
from osgeo import gdal, gdalnumeric
import gdal, ogr, os, osr
import sys
from GeoInfo import CopyMetadata
import SVM as svm
import csv



def WriteImageFromBandNum (band, tab, shape, kernel, trainingSample, validationSample):
	ar = band[0].ReadAsArray()
	cols = ar.shape[1]
	rows = ar.shape[0]
	nameBands = ""
	for i in range(len(tab)):
		nameBands+="-" + str(tab[i])
	bandName = "Bandes"+ nameBands +".tif" 
	driver = gdal.GetDriverByName('GTiff')
	outRaster = driver.Create(bandName, cols, rows, len(tab), gdal.GDT_Float32 )
	outRaster.SetProjection
	j=1
	for i in (tab):
		ar = band[i].ReadAsArray()
		outband = outRaster.GetRasterBand(j)
		outband.WriteArray(ar)
		j+=1

	outRaster.SetProjection(src.GetProjectionRef())
	outRaster.SetGeoTransform(src.GetGeoTransform())
	outband.FlushCache()
	return bandName


if (len(sys.argv) == 3) :
	image = sys.argv[1]
	shape = sys.argv[2]
	kernel = 'rbf'
	trainingSample = 500
	validationSample = 1000
	print "Default Value : kernel=rbf, trainingSample=1000, validationSample=3000"
elif (len(sys.argv)==6) :
	image = sys.argv[1]
	shape = sys.argv[2]
	kernel = sys.argv[3]
	trainingSample = sys.argv[4]
	validationSample = sys.argv[5]
else :
	print "Usage : ./SVM_main_prog.py image.tif shape.shp [OPTIONS]"
	print "OPTION : kernel(linear/rbf/poly/sigmoid) Trainig_Sample Validation_Sample"
	exit()
	


print image
src = gdal.Open(image)
print src.GetMetadata()
finalRank = open('finalRank.txt', 'w')


band=[]
tab=[]
# loop through each band
for bi in range(src.RasterCount):
	band.append(src.GetRasterBand(bi + 1))
	tab.append(bi)

tab = []
while len(tab) < len(band) :
	line = "Sélection de la bande n° " + str(len(tab)) + "\n"
	print line
	finalRank.write(line)
	tab.append(0)
	nb_band = len(tab)
	averageAccuracuy=[]
	
	for i in range(len(band)):
		tab[nb_band-1]=i
		bandName = WriteImageFromBandNum (band, tab, shape, kernel, trainingSample, validationSample)
		svm.ComputeStat(bandName)
		svm.TrainSVM (bandName, shape, kernel,trainingSample,validationSample)
		if os.path.exists("svmConfusionMatrixQB1.csv") == 0 :
			exit("svmConfusionMatrixQB1.csv n'a pas été créé")
		reader = csv.reader(open("svmConfusionMatrixQB1.csv","rb"))
		next(reader, None)
		next(reader, None)
		x=list(reader)
		confusionMatrix=np.array(x).astype('int')
		nbGood=0
		nbBad=0
		for k in range(confusionMatrix.shape[0]) :
			for j in range(confusionMatrix.shape[1]) :
				if k==j :
					nbGood+=confusionMatrix[k][j]
				nbBad+=confusionMatrix[k][j]
		averageAccuracuy.append(100 * float(nbGood)/nbBad)
		line = "   " + str(tab) + "   --->     "+ str(averageAccuracuy[i]) + "\n"
		print line
		finalRank.write(line)
	bandMax = [k for k,x in enumerate(averageAccuracuy) if x == max(averageAccuracuy)]
	line = " La bande gardée est  " + str(bandMax) + "    ;       "+ str(averageAccuracuy[bandMax[0]]) + "\n \n"
	print line
	finalRank.write(line)
	tab[nb_band-1]= bandMax[0]

finalRank.close()

print("FIN")
exit()


