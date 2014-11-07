#!/usr/bin/python
# -*- coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image 

beta=1
sigma=0.1*beta
mu=10*sigma
GausSample=np.random.normal(mu,sigma,10000)*100
GaussianSample=GausSample.reshape(100,100)
print GaussianSample
# exit()
x= np.linspace(0,32, num=100)
CosSample=beta*np.cos(x) + 1
CosineSample=np.zeros((100, 100))
for i in range(len(x)):
	for j in range(len(x)):
		CosineSample[i][j]=(i*beta*CosSample[j] +20)


# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(x, CosineSample)
# plt.xlim([0, 100])
# plt.ylim([-2,2])
# plt.xlabel("Valeurs des modules de la FFT")
# plt.ylabel("Representation des modules en pourcentage du nombre total des pixels")


im=Image.fromarray(CosineSample)

im2=Image.fromarray(np.absolute(GaussianSample))

im.show()
im2.show()
