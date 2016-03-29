#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import csv
import codecs
import json
from sklearn.cross_validation import KFold
import sys

customSplit = u"\t||\t"

reload(sys)
sys.setdefaultencoding('utf8')

def readData(path):
    sent = []
    text = []
    orgamount = 0
    actamount = 0
    with codecs.open(path,encoding= "utf-8") as f:
        next(f)  # skip headings
        file = f.read()
        file = file.split("\n")
        file = map(lambda x: x.encode("utf-8"),file)
        reader = csv.reader(file,delimiter='\t')
        for _, sen, _, tex, _ in reader:
            orgamount += 1
            if sen in ["-1", "0", "1"]:
                actamount += 1
                sent.append(int(sen))
                text.append(tex)
    comb = np.column_stack((sent, text))
    print actamount, "out of", orgamount, "is kept"
    pos = np.sum(comb[:,0] == "1")
    neg = np.sum(comb[:,0] == "-1")
    neu = np.sum(comb[:,0] == "0")
    print pos,neu,neg
    return comb


def save(result,path):
    with codecs.open(path,"a+",encoding= "utf-8") as f:
        json.dump(result,f)
        f.write("\n")

def loadRes(path):
    with codecs.open(path,"a+",encoding= "utf-8") as f:
        file = f.read()
    file = file.split("\n")
    file = map(lambda x: json.loads(x),file[0:-1])
    result = []
    for res in file:
        result.extend(res)
    return result


def saveCSV(data,path):
    with codecs.open(path,"wb+",encoding="utf-8") as f:
        for row in data:
            conc = str(row[0]) + customSplit + str(row[1]).decode("utf-8") + "\n"
            f.write(conc)

def readCustomDat(path):
    with codecs.open(path,encoding="utf-8") as f:
        file = f.read()
    file = file.split("\n")
    data = map(lambda x: x.split(customSplit),file)
    data = np.array(data[0:-1])
    return data

def strtocsv(data,delimiter = " "):
    result = str(data[0,0]) + str(delimiter) + str(data[0,1])
    for i in xrange(1,data.shape[0]):
        if len(data.shape) == 1:
            result += "\n" + str(data[i]) #.translate(string.maketrans("",""), string.punctuation)
            continue
        cols =   str(data[i,0]) + str(delimiter) + str(data[i,1])#.translate(string.maketrans("",""), string.punctuation) #+ str(delimiter) + str(row[1])
        #for j in xrange(1,data.shape[1]):
        #    cols += str(delimiter) + str(data[i,j])
        result += "\n\n" + cols
    #print result
    result = result.lower().encode("utf-8",errors='ignore')
    return result

def convert(x):
    if x == "-1":
        return "negative"
    if x == "1":
        return "positive"
    return "neutral"

def convert2(x):
    if x == "-1":
        return "1"
    if x == "1":
        return "4"
    return "3"

def preprocess(data):
    newDat = [(x[1],convert(x[0])) for x in data]
    newDat = np.array(newDat)
    return newDat

def prepDatForNer(data):
    fold = KFold(data.shape[0], n_folds=3,shuffle=True)
    data = np.array([(convert2(x[0]),x[1]) for x in data])#preprocess(data)
    current = 0
    for train_index, test_index in fold:
        pathtrain = "../nlpdat/traindat" + str(current) + ".tsv"
        pathtest = "../nlpdat/testdat" + str(current) + ".tsv"
        #with codecs.open(pathtrain,"wb+",encoding = "utf-8") as f:
        with open(pathtrain,"wb+") as f:
            asstring = strtocsv(data[train_index])
            f.write(asstring)
        with open(pathtest,"wb+") as f:
            asstring = strtocsv(data[test_index])
            f.write(asstring)
        current += 1




if __name__ == "__main__":
    data = readData("../Data/truth.tsv")
    saveCSV(data,"../Data/truth2.tsv")
    prepDatForNer(data)
