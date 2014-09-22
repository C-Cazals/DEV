#!/bin/bash


if [ "$#" != "3" ] ; then
	echo "USAGE : " $0 "image.tif shapfile.shp kernel(linear/rbf/poly/sigmoid)"
	exit
fi

image=$1
shape=$2
kernel=$3


echo Running ComputeImagesStatistics
otbcli_ComputeImagesStatistics -il $image -out  stat.xml 



echo
echo Running TrainImagesClassifier
otbcli_TrainImagesClassifier -io.il $image -io.vd $shape - -io.imstat stat.xml -sample.mv 100 -sample.mt 100  -sample.vtr 0.5 -sample.vfn Class -classifier libsvm -classifier.libsvm.k $kernel -classifier.libsvm.c 1  -classifier.libsvm.opt false -io.out svmModelQB1.svm -io.confmatout svmConfusionMatrixQB1.csv
#-sample.vtr a augmenter, 0:all training, 1:all validaition
#-sample.mv = echantillon validation
#-sample.mt = echantillon entrainement


if [ ! -f svmConfusionMatrixQB1.csv ]; then
   echo "svmConfusionMatrixQB1.csv n'a pas été créé"
   echo "exit"
   exit
fi
 echo "okkkkkkkkkkkkkkkkkk"

echo
echo Running ImageClassifier

otbcli_ImageClassifier -in $image -imstat stat.xml -model svmModelQB1.svm -out clLabeledImageQB1.tif

if [ ! -f clLabeledImageQB1.tif ]; then
   echo "clLabeledImageQB1.tif n'a pas été créé"
   echo "exit"
   exit
fi


echo
echo Running ColorMapping
 otbcli_ColorMapping -in clLabeledImageQB1.tif -method custom -method.custom.lut color_table.txt -out ColorizedClassif.tif #| echo Error exit


