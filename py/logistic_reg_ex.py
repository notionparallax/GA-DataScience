# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 23:26:49 2014

@author: mohammad
"""

''' Example Logistic regression
This code is available at
http://blog.yhathq.com/posts/logistic-regression-and-python.html
Note we used the same data when we 
did logistic regression in R
'''
#%%
import pandas as pd
import statsmodels.api as sm
import pylab as pl
import numpy as np
#%%
# read the data in
df = pd.read_csv("http://www.ats.ucla.edu/stat/data/binary.csv")
print df.head()
#%%
df.columns
#%%
#need to change the rank column name
df.columns = ["admit", "gre", "gpa", "prestige"]
df.columns
#%%
#lets have a look at the data
print df.groupby('admit').describe()
print pd.crosstab(df['admit'], df['prestige'],  rownames=['admit'])
df.hist()
#%%
dummy_ranks = pd.get_dummies(df['prestige'],  prefix='prestige')
print dummy_ranks.head()

ind_cols = ['admit', 'gre', 'gpa']
reg_data = df[ind_cols].join(dummy_ranks.ix[:, 'prestige_2':])
print reg_data.head()
reg_data['intercept'] = 1.0
print reg_data.head()
train_cols = reg_data.columns[1:]
train_cols
#%%
logit = sm.Logit(reg_data['admit'], reg_data[train_cols])
result = logit.fit()
print result.summary()
#%%
"""install these guys too
javascript-common python-gtk2-doc dvipng ipython python-configobj
  python-excelerator python-fltk python-matplotlib-doc python-traits
  python-wxgtk2.8 texlive-extra-utils texlive-latex-extra python-coverage
  python-nose-doc python-numpy-doc python-numpy-dbg python-pandas-doc
  python-tables-doc python-netcdf vitables
"""