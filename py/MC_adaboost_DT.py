# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:42:33 2014

@author: mohammad
"""

from sklearn.externals.six.moves import zip
from sklearn import metrics
import pylab as pl

from sklearn.datasets import make_gaussian_quantiles
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals.six.moves import xrange
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


# Generate some normally distributed data 10 columns with 3 groups 13000 rows.
X, y = make_gaussian_quantiles(n_samples=13000, n_features=10,
                               n_classes=3, random_state=1)
X.shape
y.shape

#Create test and train data sets 30:70
n_split = round(0.7 * len(X),0)

X_train, X_test = X[:n_split], X[n_split:]
y_train, y_test = y[:n_split], y[n_split:]

# Train the Adaboost Classifier. weak trainers with decision trees there 
# are different algorithms used

bdt_real = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=2),
    n_estimators=600,
    learning_rate=1)

bdt_discrete = AdaBoostClassifier(
    DecisionTreeClassifier(max_depth=2),
    n_estimators=600,
    learning_rate=1.5,
    algorithm="SAMME")
    
# Fit the model specified above
bdt_real.fit(X_train, y_train)
bdt_discrete.fit(X_train, y_train)


#predict clas from test dataset
bdt_real_pred = bdt_real.predict(X_test)

#show model performance on test data
print metrics.confusion_matrix(y_test , bdt_real_pred)
print metrics.accuracy_score(y_test , bdt_real_pred)
print metrics.classification_report(y_test , bdt_real_pred)

'''
Accuracy = (TP + TN) / m 
Precision =  TP / (TP +FP)
Recall =  TP / (TP + FN)
F1-score = 2 * Precision * Recall / (Precision + Recall)
support is just the number of observations in each class and total
'''

#Initiate error containers
real_test_errors = []
discrete_test_errors = []

# generate error values for iterations zip creates the pairs.
for real_test_predict, discrete_train_predict in zip(
        bdt_real.staged_predict(X_test), bdt_discrete.staged_predict(X_test)):
    real_test_errors.append(
        1. - accuracy_score(real_test_predict, y_test))
    discrete_test_errors.append(
        1. - accuracy_score(discrete_train_predict, y_test))

#for the error graph the x-axis is the iterations
n_trees = xrange(1, len(bdt_discrete) + 1)


pl.figure(figsize=(15, 5))

pl.subplot(131)
pl.plot(n_trees, discrete_test_errors, c='black', label='SAMME')
pl.plot(n_trees, real_test_errors, c='black',
        linestyle='dashed', label='SAMME.R')
pl.legend()
pl.ylim(0.18, 0.62)
pl.ylabel('Test Error')
pl.xlabel('Number of Trees')

pl.subplot(132)
pl.plot(n_trees, bdt_discrete.estimator_errors_, "b", label='SAMME', alpha=.5)
pl.plot(n_trees, bdt_real.estimator_errors_, "r", label='SAMME.R', alpha=.5)
pl.legend()
pl.ylabel('Error')
pl.xlabel('Number of Trees')
pl.ylim((.2,
        max(bdt_real.estimator_errors_.max(),
            bdt_discrete.estimator_errors_.max()) * 1.2))
pl.xlim((-20, len(bdt_discrete) + 20))

pl.subplot(133)
pl.plot(n_trees, bdt_discrete.estimator_weights_, "b", label='SAMME')
pl.legend()
pl.ylabel('Weight')
pl.xlabel('Number of Trees')
pl.ylim((0, bdt_discrete.estimator_weights_.max() * 1.2))
pl.xlim((-20, len(bdt_discrete) + 20))

# prevent overlapping y-axis labels
pl.subplots_adjust(wspace=0.25)
pl.show()