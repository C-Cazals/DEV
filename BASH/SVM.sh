#!/bin/bash


if [ "$#" -ne 2 ]; then
    echo "usage: $0 image shape "
    exit
fi

echo "Choisissez un type de noyeau : (linear/rbf/poly/sigmoid)"
read kernel

otbcli_ComputeImagesStatistics -il $1 -out Stat.xml



otbcli_TrainImagesClassifier -io.il $1 -io.vd $2 -io.imstat Stat.xml 
-sample.mv 100 -sample.mt 100
 -sample.vtr 0.5 -sample.edg false -sample.vfn Class 
-classifier libsvm -classifier.libsvm.k $kernel 
-classifier.libsvm.c 1  -classifier.libsvm.opt false
 -io.out svmModelQB1.txt -io.confmatout svmConfusionMatrixQB1.csv


#rm Stat.xml
