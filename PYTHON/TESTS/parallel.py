#!/usr/bin/python
# -*- coding: utf-8

import matplotlib.pyplot as plt
from functools import partial
 
def mandelbrotCalcRow(yPos, h, w, max_iteration = 1000):
    print(yPos)
    y0 = yPos * (2/float(h)) - 1 #rescale to -1 to 1
    row = []
    for xPos in range(w):
        x0 = xPos * (3.5/float(w)) - 2.5 #rescale to -2.5 to 1
        iteration, z = 0, 0 + 0j
        c = complex(x0, y0)
        while abs(z) < 2 and iteration < max_iteration:
            z = z**2 + c
            iteration += 1
        row.append(iteration)
 
    return row
 
def mandelbrotCalcSet(h, w, max_iteration = 1000):
    partialCalcRow = partial(mandelbrotCalcRow, h=h, w=w, max_iteration = max_iteration)
    mandelImg = map(partialCalcRow, xrange(h))
    return mandelImg

mandelImg = mandelbrotCalcSet(400, 400, 1000)
# print mandelImg
plt.imshow(mandelImg)
plt.savefig('mandelimg.jpg')