"""
The Iris dataset represents 3 kind of Iris flowers (Setosa, Versicolour
and Virginica) with 4 attributes: sepal length, sepal width, petal length
and petal width.

Principal Component Analysis (PCA) applied to this data identifies the
combination of attributes (principal components, or directions in the
feature space) that account for the most variance in the data. Here we
plot the different samples on the 2 first principal components.

"""

import pylab as pl
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA

#import data
iris = datasets.load_iris()

#initial PCA to decide on number retained
iris_PCA = PCA(copy=True)
pcas = iris_PCA.fit(iris.data)

'''
dir(pcas)
print pcas.explained_variance_
print pcas.explained_variance_ratio_

print range(1,len(pcas.explained_variance_ratio_)+1)
print pcas.explained_variance_ratio_
'''
# Create scree plot to help decide on number of PC retained
plt.plot(range(1,len(pcas.explained_variance_ratio_)+1) , pcas.explained_variance_ratio_ )
plt.xlabel('PCA in order')
plt.ylabel('Pct Variance Explained')
plt.title('PCA Scree Plot')

# how many PC's do we need to retain?

#lets apply the PCA to the data and see how the classes fall on the plot
X = iris.data
y = iris.target
target_names = iris.target_names

n_comp = 2

pca = PCA(n_components = n_comp)
X_decomp = pca.fit(X).transform(X)

print 'explained variance ratio (first two components):', \
    pca.explained_variance_ratio_

pl.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    pl.scatter(X_decomp[y == i, 0], X_decomp[y == i, 1], c=c, label=target_name)
pl.legend()
pl.title('PCA of IRIS dataset')
pl.xlabel('PCA 1')
pl.ylabel('PCA 2')
pl.show()
    

