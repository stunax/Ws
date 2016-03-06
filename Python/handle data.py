#!/usr/bin/python
# -*- coding: utf-8 -*-



import numpy as np
import glob
import json
from sklearn import linear_model
import math

def import_csv(path):
    with open(path, 'r') as f:
        file = f.readlines()
        f.close()
    words = file[0].split(",")[1:]
    file = file[1:]
    dates = map(lambda x: x.split(",")[0],file)
    data = np.array(map(lambda x: x.split(",")[1:],file),np.float)


    return words, dates, data
def load_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
    data = np.array(data[1])
    return data


def get_target_data(name):
    files = glob.glob('../data/target/' + name+ "*.json")
    data = map(load_json,files)
    data = zip(files,data)
    return data

def split_data(data,i,size,splitsize):
    newsize = (data.shape[0]-size,) + data.shape[1:]
    newDat = np.empty(newsize)
    newfold = data[i*size:(i+1)*size]
    current = 0
    for j in range(splitsize):
        if j != i:
            newDat[current:current+size] = data[j*size:(j+1)*size]
            current += size

    return newDat, newfold


def cross_valid(data,target,name ,size =12,folder=5):
    results = np.empty((folder,data.shape[1]))
    for i in range(folder):
        local_data,local_data_test = split_data(data,i,size,folder)
        local_target, local_target_test = split_data(target,i,size,folder)
        if name == "HPV" or name == "MFR"  :
            model = linear_model.LassoCV(cv=20)
            model.fit(local_data, local_target)
            results[i] = np.array(model.coef_)
        else:
            clf = linear_model.LinearRegression(fit_intercept = True)
            clf.fit(local_data, local_target)
            results[i] = np.array(clf.coef_)
    return np.mean(results,axis= 0)

def rmse(coef,data,target,name):
    inner = (np.sum(coef[None,:] * data,1) - target)**2
    outer = math.sqrt(np.sum(inner)/target.size)
    return outer

def main(name, target_name = ""):
    words,dates,data = import_csv("../data/" + name + "dat.csv")
    if target_name == "":
        target_name = name
    target_data = get_target_data(target_name)

    for vac, target in target_data:
        print vac
        coefs = cross_valid(data,target,name)
        res = rmse(coefs,data,target,name)
        print res









if __name__ == '__main__':
    main("HPV")
    #main("PCV","PVC")
    main("DiTe")
    #main("MFR","MMR")