from tulip import *
from tulipgui import *
import tulippaths as tp
import json
import random as random
output = {}
matrix = []

inputFile = open('connectivity_matrix.csv', 'r')
firstLine = True
row_labels = []
col_labels = []

for line in inputFile:
    line = line.strip('')
    array = line.split(',')
    if firstLine:
        col_labels += array[2:]
        firstLine = False
    else:
        row_labels.append(array[0])
        stringRow = array[2:len(col_labels)]
        intRow = []
        for s in stringRow:
            intRow.append(int(s))
        matrix.append(intRow)



jsonObject = {}
jsonObject['matrix'] = matrix
jsonObject['row_labels'] = row_labels
jsonObject['col_labels'] = col_labels

print json.dumps(jsonObject)
