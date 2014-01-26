# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 21:31:06 2014

@author: mohammad

In this exercise we will use the Boston House Prices data set
will will build a regression model and also a model with SVM
then compare the results of both

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.cross_validation import *
from sklearn import linear_model , svm , ensemble , metrics
from sklearn.preprocessing import StandardScaler

#load Boston datasets
bstn = load_boston()

#initial look get an understanding of the data set
dir(bstn)
bstn.DESCR
bstn.viewkeys()
bstn.feature_names
bstn.data.shape

bstn.data[1]
plt.hist(bstn.target)

# create a function to create a histogram for each input variable
def hists():
    for i in xrange(0, bstn.data.shape[1]):
        hist_var = bstn.data[i]
        x_label = bstn.feature_names[i]
        plt.hist(hist_var)
        plt.xlabel(x_label)
        plt.show()


def scatters():
    for i in xrange(0, bstn.data.shape[1]):
        x_var = bstn.data[:,i]
        x_label = bstn.feature_names[i]
        plt.scatter(x_var , bstn.target )
        plt.xlabel(x_label)
        plt.ylabel('Boston house price')
        plt.show()

       
#generate the plots
hists()
scatters()

#let move on to modelling
# First split our data into train and test
x_train , x_test , y_train , y_test = train_test_split(bstn.data ,
                                     bstn.target,
                                     test_size = 0.3,
                                     random_state = 20)


# We want to try a couple of models, for regression skewed data is not good
# we could normalise to make it a better model

x_scaler = StandardScaler().fit(x_train)
y_scaler = StandardScaler().fit(y_train)
x_train_n = x_scaler.transform(x_train)
x_test_n = x_scaler.transform(x_test)
y_test_n = y_scaler.transform(y_test)

#lets now fit a linear regression model
lm_1 = linear_model.LinearRegression(fit_intercept = True , normalize = False)
lm_1fit = lm_1.fit(x_train_n , y_train_n)
lm_1_acc = (metrics.mean_squared_error(y_train_n , lm_1fit.predict(x_train_n)))

#lets try a different regularised model
lasso_1 = linear_model.SGDRegressor(loss='squared_loss' , penalty=None, random_state=42)
lasso_1fit = lasso_1.fit(x_train_n , y_train_n)
lasso_1_acc = (metrics.mean_squared_error(y_train_n , lasso_1fit.predict(x_train_n)))

#lets fit a SVM model now
svm_def1 = svm.SVR()
svm_def1_fit = svm_def1.fit(x_train_n , y_train_n)
svm_def1_acc = (metrics.mean_squared_error(y_train_n , svm_def1_fit.predict(x_train_n)))

#try SVM with different options
svm_lin1 = svm.SVR(kernel='linear')
svm_lin1_fit = svm_lin1.fit(x_train_n , y_train_n)
svm_lin1_acc = (metrics.mean_squared_error(y_train_n , svm_lin1_fit.predict(x_train_n)))

#try SVM with different options
svm_lin05 = svm.SVR(kernel='linear' , C = 0.5)
svm_lin05_fit = svm_lin05.fit(x_train_n , y_train_n)
svm_lin05_acc = (metrics.mean_squared_error(y_train_n , svm_lin05_fit.predict(x_train_n)))

#try SVM with different options
svm_poly1 = svm.SVR(kernel='poly')
svm_poly1_fit = svm_poly1.fit(x_train_n , y_train_n)
svm_poly1_acc = (metrics.mean_squared_error(y_train_n , svm_poly1_fit.predict(x_train_n)))

#Compare results
print "svm.SVR(kernel='poly') MSE : %s."  % svm_poly1_acc
print "svm.SVR(kernel='linear' , C = 0.5) MSE : %s" % svm_lin05_acc
print "svm.SVR(kernel='linear') MSE : %s" % svm_lin1_acc
print "svm.SVR() MSE : %s" % svm_def1_acc
print "linear_model.SGDRegressor MSE : %s" % lasso_1_acc
print "linear_model.LinearRegression MSE : %s" % lm_1_acc

