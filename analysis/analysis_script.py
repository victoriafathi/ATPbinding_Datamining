# -*- coding: utf-8 -*-

import csv

file = "../data.preparation/matrix_ind_var.tsv"
source = csv.reader(open(file, 'r', encoding='utf-8'),delimiter='\t')

data = []
to_classify = []

for row in source:
    if row[-1] == "*":
        to_classify.append(row)
    else:
        data.append(row)

