# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:39:54 2014

@author: mohammad
"""

import numpy as np
from matplotlib import pylab
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold

np.random.seed(3)

# all examples will have three classes in this file
colors = ['r', 'g', 'b']
markers = ['o', 6, '*']


X = np.c_[np.ones(5), 2 * np.ones(5), 10 * np.ones(5)].T
y = np.array([0, 1, 2])

fig = pylab.figure(figsize=(10, 4))

ax = fig.add_subplot(121, projection='3d')
ax.set_axis_bgcolor('white')

mds = manifold.MDS(n_components=3)
Xtrans = mds.fit_transform(X)

for cl, color, marker in zip(np.unique(y), colors, markers):
    ax.scatter(
        Xtrans[y == cl][:, 0], Xtrans[y == cl][:, 1], Xtrans[y == cl][:, 2], c=color, marker=marker, edgecolor='black')
pylab.title("MDS on example data set in 3 dimensions")
ax.view_init(10, -15)

mds = manifold.MDS(n_components=2)
Xtrans = mds.fit_transform(X)

ax = fig.add_subplot(122)
for cl, color, marker in zip(np.unique(y), colors, markers):
    ax.scatter(
        Xtrans[y == cl][:, 0], Xtrans[y == cl][:, 1], c=color, marker=marker, edgecolor='black')
pylab.title("MDS on example data set in 2 dimensions")
