#!/bin/bash

for file in *.ecw
 do 
	file_out=`echo "$file" | cut -d'.' -f1`
	gdal_translate -of GTiff $file $file_out.tif
 done

