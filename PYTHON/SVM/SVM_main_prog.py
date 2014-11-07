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


svm.ComputeStat(image)

svm.TrainSVM(image, shape, kernel, trainingSample, validationSample)
exit()
svm.ImageClassif(image)
svm.ColorMap()
