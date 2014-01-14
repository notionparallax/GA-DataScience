#!/usr/local/bin/python

# For the code to work first
# Install graphviz (in linux use sudo apt-get install graphviz)
# pip install pyparsing 1.5.7 (sudo pip install pyparsing==1.5.7)
# pip install pydot
# reopen spyder if you installed after opening spyder


# these are part of the python standard library (psl)
from collections import Counter
import StringIO


# this is a third-party library (requires installation)
import pydot


from sklearn.datasets import load_iris
from sklearn import tree
import pandas as pd

#today we are saving our entire model build as a function!

def main():
    iris = load_iris()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(iris.data, iris.target)

    # create visualization using graphviz
    dot_data = StringIO.StringIO()
    tree.export_graphviz(clf, out_file=dot_data)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph.write_pdf('iris_dectree.pdf')
    print '\nimage created!'

    # print predictions 
    print '\npredictions:'
    print clf.predict(iris.data)

    # print Counter object with predictions (note: no training error!)
    print '\npredictions Counter:'
    print Counter(clf.predict(iris.data))

if __name__ == '__main__':
    main()

