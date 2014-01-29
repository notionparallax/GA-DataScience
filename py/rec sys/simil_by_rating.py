# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:20:46 2014

@author: mohammad
"""

from recsys.algorithm.factorize import SVD

#Create reduced dimensions via SVD
#Run SVD on the data with USERID as columns  MOVIEID as rows Ratings are values

svd = SVD()
svd.load_data(filename='./ml-1m/ml-1m/ratings.dat',
            sep='::',
            format={'col':0, 'row':1, 'value':2, 'ids': int})

# Extract 100 dimensions
# Save the SV results 
k = 100
svd.compute(k=k,
            min_values=10,
            pre_normalize=None,
            mean_center=True,
            post_normalize=True,
            savefile='./movielens')

# with similarity matrix created 
# Extract similarity between different movies

ITEMID1 = 1    # Toy Story (1995)
ITEMID2 = 2355 # A bug's life (1998)

print svd.similarity(ITEMID1, ITEMID2)

# list movies similar to a particular movie
print svd.similar(ITEMID1)
#TODO write a function to pull the movie name