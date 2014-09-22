#!/usr/bin/python 
# -*- coding: utf-8 -*- 

# Import the otb applications package 
import otbApplication 
import os


def ComputeStat (image):
	# The following line creates an instance of the ComputeImagesStatistics application 
	ComputeImagesStatistics = otbApplication.Registry.CreateApplication("ComputeImagesStatistics") 
	# The following lines set all the application parameters: 
	ComputeImagesStatistics.SetParameterStringList("il", [image]) 	 
	ComputeImagesStatistics.SetParameterString("out", "EstimateImageStatisticsQB1.xml") 
 
	# The following line execute the application 
	ComputeImagesStatistics.ExecuteAndWriteOutput()
	if os.path.exists("EstimateImageStatisticsQB1.xml") == 0 :
		exit("EstimateImageStatisticsQB1.xml n'a pas été créé")

def TrainSVM (image, shape, kernel,trainingSample,validationSample):
	cout = 1024.
	gamma = 1.
	if os.path.exists(image) == 0 :
			exit(image, " n'existe pas")
	# The following line creates an instance of the TrainImagesClassifier application 
	TrainImagesClassifier = otbApplication.Registry.CreateApplication("TrainImagesClassifier")  
	# The following lines set all the application parameters: 
	TrainImagesClassifier.SetParameterStringList("io.il", [image]) 	 
	TrainImagesClassifier.SetParameterStringList("io.vd", [shape]) 
	TrainImagesClassifier.SetParameterString("io.imstat", "EstimateImageStatisticsQB1.xml") 
	TrainImagesClassifier.SetParameterInt("sample.mv", int(validationSample)) 	 
	TrainImagesClassifier.SetParameterInt("sample.mt", int(trainingSample)) 	 
	TrainImagesClassifier.SetParameterFloat("sample.vtr", 0.5) 	 
	TrainImagesClassifier.SetParameterString("sample.edg","1") 	 
	TrainImagesClassifier.SetParameterString("sample.vfn", "Class") 	 
	TrainImagesClassifier.SetParameterString("classifier","libsvm") 	 
	TrainImagesClassifier.SetParameterString("classifier.libsvm.k",kernel) 	 
	TrainImagesClassifier.SetParameterFloat("classifier.libsvm.c", cout) 
	TrainImagesClassifier.SetParameterFloat("classifier.svm.gamma", gamma) 
	TrainImagesClassifier.SetParameterString("classifier.libsvm.opt","1") 	 
	TrainImagesClassifier.SetParameterString("io.out", "clsvmModelQB1.txt") 	 
	TrainImagesClassifier.SetParameterString("io.confmatout", "svmConfusionMatrixQB1.csv") 	 
	# The following line execute the application 
	TrainImagesClassifier.ExecuteAndWriteOutput()

def ImageClassif (image):
	# The following line creates an instance of the ImageClassifier application 
	ImageClassifier = otbApplication.Registry.CreateApplication("ImageClassifier") 
	# The following lines set all the application parameters: 
	ImageClassifier.SetParameterString("in", image) 
	ImageClassifier.SetParameterString("imstat", "EstimateImageStatisticsQB1.xml") 
	ImageClassifier.SetParameterString("model", "clsvmModelQB1.txt") 
	ImageClassifier.SetParameterString("out", "clLabeledImageQB1.tif") 
	# The following line execute the application 
	ImageClassifier.ExecuteAndWriteOutput()

def ColorMap():
	# The following line creates an instance of the ColorMapping application 
	ColorMapping = otbApplication.Registry.CreateApplication("ColorMapping") 
	# The following lines set all the application parameters: 
	ColorMapping.SetParameterString("in", "clLabeledImageQB1.tif") 
	ColorMapping.SetParameterString("method","custom") 
	ColorMapping.SetParameterString("method.custom.lut", "color_table.txt") 
	ColorMapping.SetParameterString("out", "ColorClassif.tif") 
	# The following line execute the application 
	ColorMapping.ExecuteAndWriteOutput()