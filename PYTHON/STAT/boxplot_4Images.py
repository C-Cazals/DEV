#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example boxplot code
#
import matplotlib as mpl
import matplotlib.pyplot as plt 
import csv
import sys
import numpy as np
import random

if (len(sys.argv) != 2) :
	print "Usage : ", sys.argv[0], "txt File"
	exit()

print("DEBUT")



reader=csv.reader(open(sys.argv[1]),delimiter='\t')
next(reader, None)
boolDN=0
band='0'
tab=[]
DN=[]
tab_band=[]
for row in reader:
	if len(row)==5 and 'Basic' in row[0]:
		if len(tab_band)!=0:
			tab_band.append(DN)
			DN=[]
			tab.append(tab_band)
			tab_band=[]
	if len(row)==6 and 'Histo' not in row[0]:
		if "Band" in row[0] and len(DN)!=0:
			tab_band.append(DN)
			DN=[]
		a=int(row[2])
		for it in range(a):
			if row[1]!=0:
				DN.append(float(row[1]))
tab_band.append(DN)
tab.append(tab_band)

im1=[tab[0][0], tab[1][0], tab[2][0], tab[3][0]]
im2=[tab[0][1], tab[1][1], tab[2][1], tab[3][1]]
im3=[tab[0][2], tab[1][2], tab[2][2], tab[3][2]]
im4=[tab[0][3], tab[1][3], tab[2][3], tab[3][3]]

fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20,6))
fs=10

axes[0].boxplot(im1,0,'')
axes[0].set_title('HV 21/10/2011', fontsize=fs)
axes[0].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[0].set_ylim(-30,0)

axes[1].boxplot(im2,0,'')
axes[1].set_title('HH 21/10/2011', fontsize=fs)
axes[1].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[1].set_ylim(-30,0)

axes[2].boxplot(im3,0,'')
axes[2].set_title('VV 07/09/2011', fontsize=fs)
axes[2].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[2].set_ylim(-30,0)

axes[3].boxplot(im4,0,'')
axes[3].set_title( 'HH 07/09/2011', fontsize=fs)
axes[3].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[3].set_ylim(-30,0)


plt.show()
exit('FIN')