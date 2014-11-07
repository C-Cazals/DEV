#!/bin/bash


if [ "$#" != "2" ] ; then
    echo "USAGE : " $0 "image.tif shapfile.shp"
    exit
fi

im=$1
shape=$2
image='OUT.tif'


rm -f poly.txt

rm -f lines.txt
gdalwarp -q -crop_to_cutline -dstalpha -cutline $shape $im $image


ogrinfo -al shape.shp | grep 'POLYGON' >> lines.txt

i=1
while read lines; do 
    echo $lines
    rm -f poly.txt
    xmin=10000000000
    ymin=10000000000
    xmax=0
    ymax=0
    echo $lines | grep "POLYGON" | awk -F'[()]' '{print  $3 }' | awk -F',' '{print $0}' |  sed 's/,/\n/g' >> poly.txt
    while read poly; do 
        x=$(echo -e "$poly" | awk '{ print $1}')
        y=$(echo -e "$poly" | awk '{ print $2}')

        if [ $(echo " $xmin > $x" | bc) -eq 1 ]; then
            xmin=$x
        fi
        if [ $(echo " $x > $xmax" | bc) -eq 1 ]; then
            xmax=$x
        fi
        if [ $(echo " $ymin > $y" | bc) -eq 1 ]; then
            ymin=$y
        fi
        if [ $(echo " $y > $ymax" | bc) -eq 1 ]; then
            ymax=$y
        fi
    done < poly.txt

    extent="$xmin $ymax $xmax $ymin"
    echo $extent

    nameOut="OUT${i}.tif"
    echo $nameOut

    gdal_translate -of GTiff -projwin $extent $image $nameOut
    i=$(($i+1))
done < lines.txt
