#!/usr/bin/python 
 
from pyradar.core.sar import create_dataset_from_path
from pyradar.core.sar import get_band_from_dataset
from pyradar.core.sar import get_geoinfo
from pyradar.core.sar import read_image_from_band
from pyradar.core.sar import save_image

import sys
import pyradar.core as pyr

if (len(sys.argv) == 3) :
	cu_value=0.25
	IMAGE_PATH=sys.argv[1]
	winsize=sys.argv[2]
if (len(sys.argv) == 4) :
	IMAGE_PATH=sys.argv[1]
	winsize=sys.argv[2]
	cu_value=sys.argv[3]
else:
	print("Usage : " + sys.argv[0] + " IMAGE_PATH fenetre coefficient of variation of noise default:0,25")
	exit()

