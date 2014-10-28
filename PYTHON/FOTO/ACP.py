#!/usr/bin/python
# -*- coding: utf-8

import numpy as np 
import matplotlib.pyplot as plt
import matplotlib as mpl

# notes = [[6,6],[8,8],[6,7],[14.5,14.5],[11,10],[5.5,7],[13,12.5],[9,9.5]]
notes = np.array([[6,6,5,5.5],[8,8,8,8],[6,7,11,9.5],[14.5,14.5,15.5,15],[14,14,12,12.5],[11,10,5.5,7],[5.5,7,14,11.5],[13,12.5,8.5,9.5],[9,9.5,12.5,12]]).T

print np.mean(notes[0])
print np.cov(notes)