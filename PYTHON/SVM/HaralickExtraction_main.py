#!/usr/bin/python 
 
#Import the otb applications package 
import HaralickExtraction as haral
import sys

if (len(sys.argv) == 3) :
	image = sys.argv[1]
	chan = sys.argv[2]
	xrad = 3
	yrad = 3
	print "Default Value : xrad = 3, yrad = 3"
elif (len(sys.argv)==5) :
	image = sys.argv[1]
	chan = sys.argv[2]
	xrad = sys.argv[3]
	yrad = sys.argv[4]
else :
	print "Usage : " + sys.argv[0] + " image.tif chan [OPTIONS]"
	print "OPTION : xrad, yrad"
	exit()

haral.ComputeHaralick(image, chan, xrad, yrad)