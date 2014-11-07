#!/usr/bin/python
# -*- coding: utf-8 

from pylab import *
import csv

cr = csv.reader(open("fichier.csv","rb"))

x=[]
y=[]
z=[]
for row in cr:
    x.append(int(row[0]))
    y.append(float(row[1]))
    z.append(int(row[2]))

# x = linspace(-pi, pi, 30)
# y = cos(x)
# z=sin(x)
print x


plot(x,y, 'r-x', label='y')
plot(x,z, 'y-o',label='z')
xlabel("abscisse")
ylabel("ordonn$\'{e}$es") # problème accent 

legend()
show()
