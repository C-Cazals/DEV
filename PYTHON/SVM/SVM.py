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

	ComputeImagesStatistics.SetParameterString("out", image.split('.')[0]+"_svm_EstimateImageStatistics.xml") 
 
	# The following line execute the application 
	ComputeImagesStatistics.ExecuteAndWriteOutput()
	if os.path.exists(image.split('.')[0]+"_svm_EstimateImageStatistics.xml") == 0 :
		exit(image.split('.')[0]+"_svm_EstimateImageStatistics.xml n'a pas été créé")

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
	TrainImagesClassifier.SetParameterString("io.imstat",  image.split('.')[0]+"_svm_EstimateImageStatistics.xml") 
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
	TrainImagesClassifier.SetParameterString("io.out",image.split('.')[0]+"_svm_Model.txt") 	 
	TrainImagesClassifier.SetParameterString("io.confmatout", image.split('.')[0]+"_svm_ConfusionMatrix.txt") 	 
	# The following line execute the application 
	TrainImagesClassifier.ExecuteAndWriteOutput()

def ImageClassif (image):
	# # The following line creates an instance of the ImageClassifier application 
	# ImageClassifier = otbApplication.Registry.CreateApplication("ImageClassifier") 
	# # The following lines set all the application parameters: 
	# ImageClassifier.SetParameterString("in", image) 
	# ImageClassifier.SetParameterString("imstat", image.split('.')[0]+"_svm_EstimateImageStatistics.xml") 
	# ImageClassifier.SetParameterString("model", image.split('.')[0]+"_svm_Model.txt") 
	# ImageClassifier.SetParameterString("out", image.split('.')[0]+"_svm_ClassifiedImage.tif") 
	# # The following line execute the application 
	# ImageClassifier.ExecuteAndWriteOutput()
	cmd="otbcli_ImageClassifier -in " + image + " -imstat "+ image.split('.')[0]+"_svm_EstimateImageStatistics.xml -model "+ image.split('.')[0]+"_svm_Model.txt -out "+image.split('.')[0]+"_svm_ClassifiedImage.tif"

	os.system(cmd)
	if os.path.exists(image.split('.')[0]+"_svm_ClassifiedImage.tif") == 0 :
		exit(image.split('.')[0]+"_svm_ClassifiedImage.tif was not created")

def ColorMap(image):
	# The following line creates an instance of the ColorMapping application 
	ColorMapping = otbApplication.Registry.CreateApplication("ColorMapping") 
	# The following lines set all the application parameters: 
	ColorMapping.SetParameterString("in", image.split('.')[0]+"_svm_ClassifiedImage.tif") 
	ColorMapping.SetParameterString("method","custom") 
	ColorMapping.SetParameterString("method.custom.lut", "/home/gisway/Dev/PYTHON/SVM/color_table.txt") 
	ColorMapping.SetParameterString("out", image.split('.')[0]+"_svm_ColorClassified.tif") 
	# The following line execute the application 
	ColorMapping.ExecuteAndWriteOutput()