# -*- coding: utf-8 -*-

import csv
from sklearn.ensemble import RandomForestClassifier
#from sklearn.datasets import make_classification

file = "../data.preparation/matrix_ind_var.tsv"
source = csv.reader(open(file, 'r', encoding='utf-8'),delimiter='\t')

data = []
to_classify = []

source.__next__()

for row in source:
    #rowtemp = [el for el in row]
    #for i in range(1,len(rowtemp) -1):
    #    rowtemp = float(rowtemp[i])
    #rowtemp = bool(rowtemp[-1])
    
    if row[-1] == "*":
        to_classify.append(row[1:-1])
    else:
        data.append(row)


X = [line[1:-1] for line in data]
y = [line[-1] for line in data]

print(X[0])

#X, y = make_classification(n_samples=1000, n_features=4, n_informative=2, 
#                           n_redundant=0, random_state=0, shuffle=True)

classifier = RandomForestClassifier()
classifier.fit(X,y)
print(classifier.predict(to_classify))