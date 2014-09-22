#!/bin/bash


rm photos.kml
echo "<?xml version=\"1.0\" encoding=\"utf-8\" ?>"  >> photos.kml
echo "<kml xmlns=\"http://www.opengis.net/kml/2.2\">"  >> photos.kml
echo "<Document><Folder><name>Photos</name>" >> photos.kml


for file in *.jpg
do
	rm gdal.txt

	echo "File : " $file
	echo "<Placemark>" >> photos.kml
	echo "<name>" $file "</name>" >> photos.kml
	echo "<description>sources</description>" >> photos.kml
	gdalinfo $file | grep EXIF_GPSLatitude= >> gdal.txt
	lat1=` awk '{ print $1 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	lat2=` awk '{ print $2 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	lat3=` awk '{ print $3 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	div1=`echo "$lat2/60" | bc -l`
	div2=`echo "$lat3/3600" | bc -l`
	lat=`echo $lat1+$div1+$div2  | bc`
	#echo lat $lat
	rm gdal.txt
	gdalinfo $file | grep EXIF_GPSLongitude= >> gdal.txt
	long1=` awk '{ print $1 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	long2=` awk '{ print $2 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	long3=` awk '{ print $3 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`
	div1=`echo "$long2/60" | bc -l`
	div2=`echo "$long3/3600" | bc -l`
	long=`echo $long1+$div1+$div2  | bc`
	#echo long $long
	rm gdal.txt
	gdalinfo $file | grep EXIF_GPSAltitude= >> gdal.txt
	alt=` awk '{ print $1 }' gdal.txt | cut -d')' -f1 | cut -d'(' -f2`


	echo "<Point><coordinates>"$long","$lat","$alt"</coordinates></Point>" >> photos.kml
	echo "</Placemark>" >> photos.kml

done
echo "</Folder></Document></kml>" >> photos.kml

