#!/usr/bin/python 
 
# Import the otb applications package 
import SVM as svm
import sys, getopt


if (len(sys.argv) == 3) :
	image = sys.argv[1]
	shape = sys.argv[2]
	kernel = 'rbf'
	trainingSample = 500
	validationSample = 1000
	print "Default Value : kernel=rbf, trainingSample=500, validationSample=1000"
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

print("Compute Statistics ... ")
svm.ComputeStat(image)

print("Train SVM ... ")
svm.TrainSVM(image, shape, kernel, trainingSample, validationSample)

print("Image Classification ... ")
svm.ImageClassif(image)

print("Colorizing Classification ... ")
svm.ColorMap(image)


