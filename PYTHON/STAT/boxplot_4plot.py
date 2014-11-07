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
			DN=[]
		a=int(row[2])
		for it in range(a): DN.append(row[1])
tab_band.append(DN)
tab.append(tab_band)


data1=np.array(tab[0]).astype('float').transpose()
data2=np.array(tab[1]).astype('float').transpose()
data3=np.array(tab[2]).astype('float').transpose()
data4=np.array(tab[3]).astype('float').transpose()

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(6,6))
fs=10

axes[0, 0].boxplot(data1,0,'')
axes[0, 0].set_title(u'Foret agée', fontsize=fs)
axes[0, 0].set_xticklabels(['HV 21/10/2011', 'HH 21/10/2011', 'VV 07/09/2011', 'HH 07/09/2011'])

axes[0, 1].boxplot(data2,0,'')
axes[0, 1].set_title('Foret jeune', fontsize=fs)
axes[0, 1].set_xticklabels(['HV 21/10/2011', 'HH 21/10/2011', 'VV 07/09/2011','HH 07/09/2011'])

axes[1, 0].boxplot(data3,0,'')
axes[1, 0].set_title('Sol nu', fontsize=fs)
axes[1, 0].set_xticklabels(['HV 21/10/2011', 'HH 21/10/2011','VV 07/09/2011', 'HH 07/09/2011'])

axes[1, 1].boxplot(data4,0,'')
axes[1, 1].set_title( u'Végétation  basse', fontsize=fs)
axes[1, 1].set_xticklabels(['HV 21/10/2011', 'HH 21/10/2011', 'VV 07/09/2011','HH 07/09/2011'])

	
plt.show()
exit('FIN')
