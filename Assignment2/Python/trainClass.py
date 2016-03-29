#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import multiprocessing as mp
from readData import *
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import pickle
import os
from sklearn.cross_validation import KFold

def save_classifier(classifiers):
    f = open('../Data/Models.pickle', 'wb')
    pickle.dump(classifiers, f, -1)
    f.close()

def load_classifier():
    f = open('../Data/Models.pickle', 'rb')
    results= pickle.load(f)
    f.close()
    return results

def fold3(data):
    #Missing last, missing middle, missing first part
    fold = KFold(data.shape[0], n_folds=3,shuffle=True)
    result = []
    for train_index, test_index in fold:
        result.append((data[train_index],test_index))
    #result = [data[0:(n/3*2)],data[0:(n/3)] + data[(n/3*2):-1],data[(n/3):-1]]
    return result

def toblob(data):
    return map(lambda x: (TextBlob(x[0]),TextBlob(x[1])),data)

def train(data):
    result = []
    for dat,test_index in fold3(data):
        result.append((NaiveBayesClassifier(toblob(dat)),test_index))
    return result

def correctpred(dat,res):
    res = "neutral"
    correct = dat[1] == "neutral"
    if sum([x == "negative" for x in res]) > 1:
        res = "negative"
        correct = dat[1] == "negative"
    if sum([x == "positive" for x in res]) > 1:
        res = "positive"
        correct = dat[1] == "positive"
    return res,correct


def test(models,data):
    current = 0
    result = []
    for model,test_index in models:
        print "fold",current
        testdat = toblob(data[test_index])
        result.append(model.accuracy(testdat))
        current += 1
    result = round(np.mean(result)*100,2)
    print result,"percentage"
    #print correct,"/",len(data),"(",round(1.*correct/len(data)*100,2),"%)"
    return result

if __name__ == "__main__":
    data = readCustomDat("../Data/truth2.tsv")
    data = preprocess(data)
    #check if one of the models exist. Assume alle other models exists, if first does
    if __debug__ or not os.path.isfile('../Data/Model2.pickle'):
    #if __debug__ or not os.path.isfile('../Data/Model2.pickle'):
        print "Training on data"
        models = train(data)
        save_classifier(models)
        print "Training concluded. Starting classification"
    else:
        print "Model found on disc"
        models = load_classifier()
        print "Model loaded from disc!"
    print "Measuring accuracy"
    result = test(models, data)
