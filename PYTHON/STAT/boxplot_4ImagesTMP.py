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
	print "Usage : ", sys.argv[0], "csvFile"
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
			
			
			print len(DN)
			DN=[]

		a=int(row[2])
		for it in range(a):
			if row[1]!=0:
				DN.append(row[1])
tab_band.append(DN)
print len (DN)

tab.append(tab_band)
print len(tab[3][0])
bla1=[]
DN1=[]
bla2=[]
DN2=[]
bla3=[]
DN3=[]
bla4=[]
DN4=[]

for k in range(4):
	for j in range(min(len(tab[0][0]), len(tab[1][1]), len(tab[2][2]), len(tab[3][3]))):
		bla1.append(tab[0][k][j])
		bla2.append(tab[1][k][j])
		bla3.append(tab[2][k][j])
		bla4.append(tab[3][k][j])
	DN1.append(bla1)
	bla1=[]
	DN2.append(bla2)
	bla2=[]
	DN3.append(bla3)
	bla3=[]
	DN4.append(bla4)
	bla4=[]
data1=np.array(DN1).astype('float').transpose()
data2=np.array(DN2).astype('float').transpose()
data3=np.array(DN3).astype('float').transpose()
data4=np.array(DN4).astype('float').transpose()

fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(20,6))
fs=10


axes[0].boxplot(data1,0,'')
axes[0].set_title('HV 21/10/2011', fontsize=fs)
axes[0].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[0].set_ylim(-30,0)

axes[1].boxplot(data2,0,'')
axes[1].set_title('HH 21/10/2011', fontsize=fs)
axes[1].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[1].set_ylim(-30,0)

axes[2].boxplot(data3,0,'')
axes[2].set_title('VV 07/09/2011', fontsize=fs)
axes[2].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[2].set_ylim(-30,0)

axes[3].boxplot(data4,0,'')
axes[3].set_title( 'HH 07/09/2011', fontsize=fs)
axes[3].set_xticklabels(['Fa', 'Vb', 'Fj','Sn'])
axes[3].set_ylim(-30,0)


plt.show()
exit('FIN')
