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
    for i in xrange(3):
        classifier = classifiers[i]
        f = open('../Data/Model' + str(i) + '.pickle', 'wb')
        pickle.dump(classifier, f, -1)
        f.close()

def load_classifier():
    results = []
    for i in xrange(3):
        f = open('../Data/Model' + str(i) + '.pickle', 'rb')
        results.append(pickle.load(f))
        f.close()
    return results

def convert(x):
    if x == "-1":
        return "negative"
    if x == "1":
        return "positive"
    return "neutral"

def preprocess(data):
    newDat = [(x[1],convert(x[0])) for x in data]
    newDat = np.array(newDat)
    return newDat

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

def doclassification(data):
    print "next"
    return NaiveBayesClassifier(data)

def train(data):
    result = []
    for dat,test_index in fold3(data):
        result.append((doclassification(toblob(dat)),test_index))
    #result = [doclassification(x) for x in fold3(data)]
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
        print "Model",current
        testdat = toblob(data[test_index])
        result.append(model.accuracy(testdat))
        current += 1
    result = round(np.mean(result)*100,2)
    #for dat in data:
    #    res = [models[0].classify(dat[0]),models[1].classify(dat[0]),models[2].classify(dat[0])]
    #    tmp = correctpred(dat,res)
    #    correct += tmp[1]
    #    result.append(tmp[0])
    print result,"percentage"
    #print correct,"/",len(data),"(",round(1.*correct/len(data)*100,2),"%)"
    return result

if __name__ == "__main__":
    data = readCustomDat("../Data/truth2.tsv")
    data = preprocess(data)


    #check if one of the models exist. Assume alle other models exists, if first does
    if not os.path.isfile('../Data/Model2.pickle'):
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
