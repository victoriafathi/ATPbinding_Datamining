#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz

#from sklearn.datasets import make_classification

file = "../data.preparation/matrix_ind_var.tsv"
source = csv.reader(open(file, 'r', encoding='utf-8'),delimiter='\t')

data = []
to_classify = []

header = source.__next__()

for row in source:
    if row[-1] == "*":
        to_classify.append(row[1:-1]) #data to classify
    else:
        data.append(row) #training data


X = [line[1:-1] for line in data]
y = [line[-1] for line in data] # classes

print(X[0])

#X, y = make_classification(n_samples=1000, n_features=4, n_informative=2, 
#                           n_redundant=0, random_state=0, shuffle=True)

classifier = RandomForestClassifier()
classifier.fit(X,y)
test = classifier.estimators_[5]

export_graphviz(test, 
                out_file='tree.dot', 
                feature_names = header[1:-1],
                rounded = True, proportion = False, 
                precision = 2, filled = True)

from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

from IPython.display import Image
Image(filename = 'tree.png')

print(classifier.predict(to_classify))
