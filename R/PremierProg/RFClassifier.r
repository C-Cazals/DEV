##########################################################################################
##
## RFClassifier - A script for classifying remote sensing images using Random Forests.
##
## Jefferson Ferreira-Ferreira (jefferson.ferreira@mamiraua.org.br) - Mamirauá Sustainable
## Development Institute, Tefé, AM, Brazil. www.mamiraua.org.br
##
## Thiago Sanna Freire Silva (tsfsilva@rc.unesp.br) - Geography Department, São Paulo State
## university (UNESP), Rio Claro, SP, Brazil. http://www.rc.unesp.br/igce/geografia/
## 
## January 30th, 2014.
##########################################################################################
##
## To learn more about Random Forests,  see Breiman L (2001) Random Forests. Machine
## Learning, vol. 45(1), pp.5-32 and Liaw A, Wierner M (2002) Classification and regression
## by random-Forest. RNews, vol. 2/3, pp. 18-22.
##
## To learn more about object-oriented classification, see Blaschke T et al. (2014) Geographic
## Object-Based Image Analysis – Towards a new paradigm. ISPRS J. Photogramm. Remote Sens. 
## vol. 87, pp. 180–191.
## 
## This script requires the following R packages: rgdal, randomForest
##
## To know more about the randomForests R package, visit:
## http://cran.r-project.org/web/packages/randomForest/index.html
##
## A full citation for any R package can be obtained by typing citation('package.name')
## A full citation for the main R software can be obtained by typing citation('base')
##
## This script was tested using R 3.0.2, randomForest 4.6-7, and rgdal 0.8-8
##
## Input files are shapefiles representing the objects resulting from an image
## segmentation algorithm (e.g. eCognition - www.ecognition.com, GeoDMA - 
## http://sourceforge.net/apps/mediawiki/geodma, InterIMAGE - http://www.lvc.ele.puc-rio.br/projects/interimage/)
## 
## The attribute colums of the shapefile are the object features/predictive variables that
## will serve as inputs for the classification algorithm (e.g. mean reflectance or radar
## backscattering,standard deviation, form descriptors, etc). In addition to these predictive
## variables, one additional column must be present, labelling some of the objects (records)
## according to their observed class (training samples), and the remaining objects as
## "unclassified" or a similar notation. For example:
## 
##  FID Mean1 Mean2 Mean3 Sd1 Sd2 Sd3 class
##  0   2956  3456  4325  345 348 213 water
##  
## Note that the quantity of training samples will affect the final accuracy of the
## classification, and the OOB error estimation. You should work iteratively with the number
## of trees, the number of randomly selected predictive variables and the number of
## samples, until an acceptable OOB Error is reached. 
##
##############################################################################################
##############################################################################################

# Set your working directory here
setwd(".")

# Load required packages. If not yet installed, use: 
# install.packages(c('rgdal','randomForest'),dependencies=TRUE)
library(rgdal)
library(randomForest)

# Load input data
# "dsn" is the full path to the shapefile, "layer" is the file name, without extension
# Replace path and file names appropriately.
shape <- readOGR(dsn="C:/shapes/segments.shp", layer="segments")

# "classes" is our column identifiying the classified training samples
# Replace "classes" by the appropriate column name in your shapefile 

# Classes should be converted to factor for proper use of randomForest
shape$classes <- factor(shape$classes)

# You may inspect class names to make sure everything is correct
summary(shape$classes)

# Here you select only the training samples in the loaded shapefile, which will train 
## the classifier. 'un' is the label identifying all unclassified records
## != 'un' means "different than unclassified".
training <- shape[shape$classes != 'un',]

# Subsetting a data frame in R keeps all the factor levels, even if there are no
# observations for that level. 
levels(training$classes)

# We recast the variable as a factor to remedy that
training$classes <- factor(training$classes)
levels(training$classes)

## RANDOM FOREST CLASSIFICATION

# TRAINING THE CLASSIFIER
# randomForest uses a formula notation, similar to a lm() regression model .
# The variable to be predicted (class_RF) goes on the left, and the predictors on the right
# the dot (.) means "all variables"
# The set.seed parameter fixes the random number generation, to allow repeatability of
# the results. Without setting this number, a different random sample of variables will be
# selected every time the algorithm is executed, yileding slighlty variable results. Any
# value can be chosen for set.seed, as long as it is kept equal between runs.
#
# "ntree" is the desired number of random trees to be generated and "mtry" is the number of
# variables to be randomly sampled as candidates at each split in each tree. The default value
# for "mtry" is the square root of your total number of predicitive variables (attributes).
# We suggest you start with a lower number of trees, such as 200, and iteratively test it
# in combination with "mtry" and with increasing the size of your training sample.
# The parameters specified below correspond to the ideal configuration obtained for the
# mapping of wetland vegetation classes in the Mamirauá Sustainable Development Reserve, 
# Central Amazon, Brazil, using ALOS/PALSAR images.

r_tree <- randomForest(classes ~ ., data = training, set.seed=123,ntree =5000,mtry=20)

# Shows a confusion matrix derived from OOB comparisons.
r_tree


# You can also inspect the conditional variable importance, i.e. the level of importance of 
# each variable for determining each split in each tree. 
# "type = 1" means decrease in accuracy, "type=2" means decrease in node impurity

varimp <- importance(r_tree, type=1)

# Check the variable importance matrix and plot the results
varimp
varImpPlot(r_tree)

# You can write it to a csv file, which can be useful for further analysis
write.table(varimp, file="varimp.csv",sep=";")

# If your are satisfied with the OOB estimated error, apply the classifier to all samples.
# It will produce a vector of resulting class names

classified <- predict(r_tree, shape)

# Check how many objects were assigned to each class
summary(classified)

# Now, you can append the classification results back into the original shapefile, as a new
# column

shape$classified <-  classified

# Finally, save the classification results as a new shapefile
writeOGR(shape,dsn="classified.shp", layer = "classified", driver="ESRI Shapefile")


## END