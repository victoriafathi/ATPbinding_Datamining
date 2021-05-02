#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from sklearn import tree


#from sklearn.datasets import make_classification

file = "data.preparation/matrix_ind_var.tsv"
source = csv.reader(open(file, 'r', encoding='utf-8'),delimiter='\t')

data = []
to_classify = []

header = source.__next__()

for row in source:
    if row[-1] == "*":
        to_classify.append(row[1:-1]) #data to classify
    else:
        data.append(row) #training data

print("Data charged")

# Matrix manipulation functions
def split_table(t,indicatrix):
    """
    Splits a table t into 2 according to an incatrix.
    In other words, returns a couple of lists (t0, t1), where :
        - if indicatrix[i] contains True, then t[i] is in t1.
        - else, t[i] is in t0.
        
    Here, an indicatrix is a list of booleans the same length as t.
    """
    t0 = []
    t1 = []
    for i in range(len(t)):
        if indicatrix[i]:
            t1.append(t[i])
        else:
            t0.append(t[i])
    return(t0,t1)

def extract_columns(data, columns):
    """
    Extracts columns from data 
    """
    selected_data = []
    for line in data:
        selected_row = []
        for i in columns:
            selected_row.append(line[i])
        selected_data.append(selected_row)

    return selected_data

X_columns = range(1,len(data[0])-1)
y_columns = [len(data[0])-1]

X_total = extract_columns(data, X_columns)
y_total = extract_columns(data, y_columns) # Classes
y_indicatrix = [int(i[0]) for i in y_total]

#X = [line[1:-1] for line in data]
#y = [line[-1] for line in data] # classes

# Splitting data between abc and not abc
data_non_abc, data_abc = split_table(data,y_indicatrix)

induviduals_per_class = len(data_abc)

selected_non_abc_index = np.random.choice(
        len(data_non_abc),induviduals_per_class, replace=False)
selected_non_abc_indicatrix = [
        (i in selected_non_abc_index) for i in range(len(data_non_abc))]

data_non_abc_non_selected, data_non_abc_selected = split_table(
        data_non_abc,selected_non_abc_indicatrix)

data_reduced = []
data_reduced.extend(data_abc)
data_reduced.extend(data_non_abc_selected)

X_reduced = extract_columns(data_reduced, X_columns)
y_reduced = extract_columns(data_reduced, y_columns)

X_non_abc = extract_columns(data_non_abc_non_selected, X_columns)
y_non_abc = extract_columns(data_non_abc_non_selected, y_columns)


print("Data separation finished")
#X, y = make_classification(n_samples=1000, n_features=4, n_informative=2, 
#                           n_redundant=0, random_state=0, shuffle=True)
print("\n=============================================\n")
print("Full set training")

X_total_train, X_total_test, y_total_train, y_total_test = train_test_split(
        X_total, y_total, test_size=0.3) # 70% training and 30% test

y_total_train = np.ravel(y_total_train)
y_total_test = np.ravel(y_total_test)

classifier_total = RandomForestClassifier(
        criterion = "entropy", max_depth = 6, n_jobs = 6, n_estimators = 10)
classifier_total.fit(X_total_train,y_total_train)

print("Classifier trained")

print()
print("Results:")

print("Test set")
y_total_test_pred=classifier_total.predict(X_total_test)
print(classification_report(y_total_test, y_total_test_pred, 
                            target_names = ["Not ABC", "ABC"]))

print("Training set")
y_total_train_pred=classifier_total.predict(X_total_train)
print(classification_report(y_total_train, y_total_train_pred, 
                            target_names = ["Not ABC", "ABC"]))


print("Prediction of data to predict")
print(classifier_total.predict(to_classify))

#print("\n=============================================\n")
#print("Balanced Training set")
#
#X_train, X_test, y_train, y_test = train_test_split(
#        X_reduced, y_reduced, test_size=0.3) # 70% training and 30% test
#
#y_train = np.ravel(y_train)
#y_test = np.ravel(y_test)
#
#classifier = RandomForestClassifier(oob_score = True, criterion = "entropy")
#classifier.fit(X_train,y_train)
#
#print("Classifier trained")
#
#print()
#print("Results:")
#
#print("Test set")
#y_test_pred=classifier.predict(X_test)
#print(classification_report(y_test, y_test_pred, 
#                            target_names = ["Not ABC", "ABC"]))
#
#print("Training set")
#y_train_pred=classifier.predict(X_train)
#print(classification_report(y_train, y_train_pred, 
#                            target_names = ["Not ABC", "ABC"]))


#print("Prediction of data to predict")
#print(classifier.predict(to_classify))

#print("Non ABC set")
#y_non_abc_pred=classifier.predict(X_non_abc)
#print(classification_report(y_non_abc, y_non_abc_pred, target_names = ["Not ABC", "ABC"]))


plt.figure(figsize=(100,100)) 
_ = tree.plot_tree(classifier_total.estimators_[0], feature_names = header[:-1],
            filled=True, fontsize=6, rounded = True)
plt.savefig('filename.png')

