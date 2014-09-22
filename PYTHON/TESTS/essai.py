#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pylab import *
from PIL import Image
import numpy as np

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

def filtreMed(raster, out):
    rasterx = raster.size[0]
    rastery = raster.size[1]
    #print rasterx,rastery
    li=[]   
    for i in range(1,rasterx-2,1):
        for j in range(1, rastery-2,1):
            for m in range(-1, 1,1):
                for n in range(-1, 1,1):
                    li.append(raster.getpixel((i+m,j+n)))
            a= median(li)
            li = []
            out.putpixel((i,j), (a))
    return out

def histogramme(raster):
    histo = zeros(256)
    for i in range(0, raster.size[0]):
        for j in range(0, raster.size[1]):
            histo[raster.getpixel((i,j))]+=1
    return histo


print("DEBUT")

tab=[1, 8 , 0, 6 , 8, 0 ,18]

print tab
a= np.nonzero(tab)
# b= np.delete(tab, a)
print a

b=np.delete(tab,2)

print b

exit("FIN")
tab = []

for k in range(3):
    tab.append(0)
    for i in range(3) :
        tab[k]=i
        print int(tab[0])









exit("FIN")







#ouverture de l'image et gestion des erreurs éventuelles

try:
    raster = Image.open("test_Python.tif")
except IOError:
    print "impossible d'ouvrir le fichier"
    sys.exit()
#informations diverses
#print raster.format, raster.size, raster.mode, raster.info

histo = histogramme(raster)
x=arange(0,histo.size, 1)
plot(x, histo)
ylim(0,800)

show()
# out = Image.new('1', (raster.size[0], raster.size[1]), "black")
# filtreMed(raster, out)
# out.show()

#raster.show()


#worldfile = open('test_Python.tfw', "r")
#print worldfile.read()
