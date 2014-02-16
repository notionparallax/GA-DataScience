# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 12:50:33 2014

@author: mohammad
"""

from sklearn import tree, datasets , metrics , svm
import numpy as np
import pylab as pl
from sklearn.utils import shuffle


iris = datasets.load_iris()
X, y = iris.data, iris.target
dir(iris)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)


print(metrics.classification_report(y, clf.predict(X), target_names=iris.target_names))
fpr, tpr, thresholds = metrics.roc_curve(y, clf.predict(X) , average = 'macro')



# example on Iris dataset Binary outcome only
random_state = np.random.RandomState(0)


# Make it a binary classification problem by removing the third class
X, y = X[y != 2], y[y != 2]
n_samples, n_features = X.shape


# shuffle and split training and test sets
X, y = shuffle(X, y, random_state=random_state)
half = int(n_samples / 2)
X_train, X_test = X[:half], X[half:]
y_train, y_test = y[:half], y[half:]

# Run classifier
classifier = svm.SVC(kernel='linear', probability=True, random_state=0)
probas_ = classifier.fit(X_train, y_train).predict_proba(X_test)

# Compute ROC curve and area the curve
fpr, tpr, thresholds = metrics.roc_curve(y_test, probas_[:, 1])
roc_auc = metrics.auc(fpr, tpr)
print("Area under the ROC curve : %f" % roc_auc)

# Plot ROC curve
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver operating characteristic example')
pl.legend(loc="lower right")
pl.show()
