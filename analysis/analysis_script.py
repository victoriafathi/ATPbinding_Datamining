#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import csv
import numpy as np
import argparse

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from sklearn import tree

def import_data(filepath):
    """Imports csv table from filepath. 
    Returns a tuple containing in order:
        - Table header
        - Labeled data
        - Unlabeled data (to classify)"""

    source = csv.reader(open(filepath, 'r', encoding='utf-8'),delimiter='\t')
    
    data = []
    to_classify = []
    
    header = source.__next__()
    
    for row in source:
        if row[-1] == "*":
            to_classify.append(row) #data to classify
        else:
            data.append(row) #training data
    
    
    return (header, data, to_classify)
    

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

def extract_data(data, X_columns, y_columns, mode):
    X_total = extract_columns(data, X_columns)
    y_total = extract_columns(data, y_columns)
    
    if mode == 'full':
        X = X_total
        y = y_total
    else:
        # Splitt data between abc and not abc
        y_indicatrix = [int(i[0]) for i in y_total]
        data_non_abc, data_abc = split_table(data,y_indicatrix)
        
        # Number of ABC genes
        induviduals_per_class = len(data_abc)
        
        # Reduce to the number of non-ABC genes
        selected_non_abc_index = np.random.choice(
                len(data_non_abc),induviduals_per_class, replace=False)
        
        selected_non_abc_indicatrix = [
                (i in selected_non_abc_index) for i in range(len(data_non_abc))]
        
        _, data_non_abc_selected = split_table(
                data_non_abc,selected_non_abc_indicatrix)
        
        # Concatenate the data for the two classes
        data_reduced = []
        data_reduced.extend(data_abc)
        data_reduced.extend(data_non_abc_selected)
        
        X = extract_columns(data_reduced, X_columns)
        y = extract_columns(data_reduced, y_columns)
        
    
    return X,y
###############################################################################

if __name__=="__main__":
    
    # Parser arguments
    parser = argparse.ArgumentParser(description='Analysis')
    parser.add_argument('-m', '--mode', choices=['full', 'balanced'], 
        default='full', required=False, 
        help='Train on full set or balanced set (default : full set)')
    parser.add_argument('-d','--max_depth', type=int, default=None, 
        required=False, help='max depth of the each tree (default : None)')
    parser.add_argument('-n','--n_estimators', type=int, default=100, 
        required=False, help='number of estimators (default:100)')
    parser.add_argument('-c','--criterion', choices=['gini','entropy'], 
        default='entropy', required=False,
        help='function to measure the quality of a split. ' 
        + 'Supported criteria are “gini” for the Gini impurity ' 
        + 'and “entropy” for the information gain (default: entropy)')
    parser.add_argument('-b','--base', type=str, required=False, 
        default='results', help='base of the filenames in which the results '
        + 'are stored, without any extensions.')
    parser.add_argument('-t','--save_trees', required=False, 
        action="store_true", help='include if the trees should be plotted')
    parser.add_argument('-s','--seed', required=False, type=int, default=1148823,
        help='32-bit integer to seed the run (default: 1148823)')
    
    args = parser.parse_args()
    
    np.random.seed(args.seed)    
    
    # Data loading
    infile = "data.preparation/matrix_ind_var.tsv"
    (header, data, to_classify) = import_data(infile)
    print("Data loaded")
    
    # Indexes of relevant columns for variables (X) and classes (y)
    X_columns = range(1,len(data[0])-1)
    y_columns = [len(data[0])-1]
    
    # Only take the variable columns
    to_classify = extract_columns(to_classify, X_columns)
    
    X,y = extract_data(data, X_columns, y_columns, args.mode)
    
    # Separate train and test sets : 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    print("Data perpared")
    
    # creating and training the random forest
    classifier = RandomForestClassifier( criterion=args.criterion, 
        max_depth=args.max_depth, n_estimators = args.n_estimators)
    
    classifier.fit(X_train,y_train)
    print("Classifier trained")

    y_test_pred=classifier.predict(X_test)
    
    report = classification_report(y_test, y_test_pred, 
                                target_names = ["Not ABC", "ABC"])
    
    to_classify_pred = classifier.predict(to_classify)
    
    #print(to_classify)
    
    print("\n=============================================\n")
    print("Results:")

    print(report)
        
    print("Prediction of data to predict:")
    print(to_classify_pred)
    
    # Write the report
    out = open(str.format('analysis/{}_report.txt',args.base), 'w', encoding='utf-8')
    out.write("=============================================\n")
    out.write("Results:")

    out.write(report)
        
    out.write("Prediction of data to predict:")
    out.write(str(to_classify_pred))
    
    out.close()

    # Save the trees
    if args.save_trees:
        for i in range(args.n_estimators):
            plt.figure(figsize=(350,90), dpi = 80) 
            tree.plot_tree(classifier.estimators_[i], feature_names = header[1:-1],
                           filled=True, fontsize=70, rounded = True)
            plt.savefig(str.format('analysis/{}{}.pdf',args.base,i), dpi=1200, 
                        format='pdf', bbox_inches='tight')

