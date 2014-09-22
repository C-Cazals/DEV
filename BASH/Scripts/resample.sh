
#!/bin/bash

for file in ../*.tif
 do 
	file_out=`echo "$file"  | cut -d'/' -f2 | cut -d'.' -f1`
	echo $file_out	
	gdalwarp -of GTiff -ts 1000 1000  -s_srs EPSG:2154 -t_srs EPSG:32631 -r bilinear $file $file_out"_Resampled.tif"

 done



