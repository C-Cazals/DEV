#!/usr/bin/python 
# -*- coding: utf-8 -*-

# Import the otb applications package 
import otbApplication 
 
def ComputeHaralick(image, chan, xrad, yrad):

	# The following line creates an instance of the HaralickTextureExtraction application 
	HaralickTextureExtraction = otbApplication.Registry.CreateApplication("HaralickTextureExtraction") 
	# The following lines set all the application parameters: 
	HaralickTextureExtraction.SetParameterString("in", image) 
	HaralickTextureExtraction.SetParameterInt("channel", int(chan))
	HaralickTextureExtraction.SetParameterInt("parameters.xrad", int(xrad)) 
	HaralickTextureExtraction.SetParameterInt("parameters.yrad", int(yrad)) 	 
	HaralickTextureExtraction.SetParameterString("texture","simple") 
	HaralickTextureExtraction.SetParameterString("out", "HaralickTextures.tif") 	 
	# The following line execute the application 
	HaralickTextureExtraction.ExecuteAndWriteOutput()
	print "HaralickTextures.tif a été écrit"

