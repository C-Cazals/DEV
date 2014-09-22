#!/bin/bash


if [ "$#" != "2" ] ; then
	echo "USAGE : " $0 "image.tif shapfile.shp"
	exit
fi

image=$1
shape=$2



echo Running ComputeImagesStatistics
otbcli_ComputeImagesStatistics -il $image -out  stat.xml 



echo
echo Running TrainSVMImagesClassifier
#otbcli_TrainSVMImagesClassifier -io.il $image -io.vd $shape -io.imstat stat.xml  -io.out svmModel.svm #Classif avec kernel lineaire
otbcli_TrainSVMImagesClassifier -io.il $image -io.vd $shape - -io.imstat stat.xml -svm.k rbf -svm.opt 1 -sample.vtr 0.5 -io.out svmModel.svm


#-sample.vtr a augmenter, 0:all training, 1:all validaition


echo
echo Running ImageSVMClassifier
otbcli_ImageSVMClassifier -in $image -imstat stat.xml -svm svmModel.svm -out classif.tif float
 #| echo Error exit

echo
echo Running ColorMapping
 otbcli_ColorMapping -in classif.tif -method custom -method.custom.lut color_table.txt -out ColorizedClassif.tif #| echo Error exit




