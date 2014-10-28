#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from pylab import *
from PIL import Image
import numpy as np



from pylab import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes

# function for setting the colors of the box plots pairs
def setBoxColors(bp):
    setp(bp['boxes'][0], color='blue')
    setp(bp['caps'][0], color='blue')
    setp(bp['caps'][1], color='blue')
    setp(bp['whiskers'][0], color='blue')
    setp(bp['whiskers'][1], color='blue')
    setp(bp['fliers'][0], color='blue')
    setp(bp['fliers'][1], color='blue')
    setp(bp['medians'][0], color='blue')

    setp(bp['boxes'][1], color='red')
    setp(bp['caps'][2], color='red')
    setp(bp['caps'][3], color='red')
    setp(bp['whiskers'][2], color='red')
    setp(bp['whiskers'][3], color='red')
    setp(bp['fliers'][2], color='red')
    setp(bp['fliers'][3], color='red')
    setp(bp['medians'][1], color='red')

# Some fake data to plot
A= [[1, 2, 5,],  [7, 2]]
B = [[5, 7, 2, 2, 5], [7, 2, 5]]
C = [[3,2,5,7], [6, 7, 3]]

fig = figure()

hold(True)

# first boxplot pair
bp = boxplot(A, positions = [1, 2], widths = 0.6)
setBoxColors(bp)
show()
# def median(mylist):
#     sorts = sorted(mylist)
#     length = len(sorts)
#     if not length % 2:
#         return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
#     return sorts[length / 2]

# def filtreMed(raster, out):
#     rasterx = raster.size[0]
#     rastery = raster.size[1]
#     #print rasterx,rastery
#     li=[]   
#     for i in range(1,rasterx-2,1):
#         for j in range(1, rastery-2,1):
#             for m in range(-1, 1,1):
#                 for n in range(-1, 1,1):
#                     li.append(raster.getpixel((i+m,j+n)))
#             a= median(li)
#             li = []
#             out.putpixel((i,j), (a))
#     return out

# def histogramme(raster):
#     histo = zeros(256)
#     for i in range(0, raster.size[0]):
#         for j in range(0, raster.size[1]):
#             histo[raster.getpixel((i,j))]+=1
#     return histo


# print("DEBUT")

# CLIP = sys.argv[2]
# inRaster = sys.argv[1]
# outRaster = "OUT.tif"

# cmd = 'gdalwarp -q -te a b c d -cutline %s -crop_to_cutline %s %s' % (CLIP, inRaster, outRaster)

# os.system(cmd)
# cmd = 'echo $a'
# os.system(cmd)
# exit("FIN")

# tab=[1, 8 , 0, 6 , 8, 0 ,18]

# print tab
# a= np.nonzero(tab)
# # b= np.delete(tab, a)
# print a

# b=np.delete(tab,2)

# print b

# exit("FIN")
# tab = []

# for k in range(3):
#     tab.append(0)
#     for i in range(3) :
#         tab[k]=i
#         print int(tab[0])









# exit("FIN")







# #ouverture de l'image et gestion des erreurs éventuelles

# try:
#     raster = Image.open("test_Python.tif")
# except IOError:
#     print "impossible d'ouvrir le fichier"
#     sys.exit()
# #informations diverses
# #print raster.format, raster.size, raster.mode, raster.info

# histo = histogramme(raster)
# x=arange(0,histo.size, 1)
# plot(x, histo)
# ylim(0,800)

# show()
# # out = Image.new('1', (raster.size[0], raster.size[1]), "black")
# # filtreMed(raster, out)
# # out.show()

# #raster.show()


# #worldfile = open('test_Python.tfw', "r")
# #print worldfile.read()
