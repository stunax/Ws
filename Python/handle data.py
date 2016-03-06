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

    model = linear_model.LassoCV(cv=5,positive=True)
    model.fit(data, target)
    lassores = model
    #Other models!
    #No other used.


    result = lassores #+ other models
    return result,

def rmse(models,data,target,name):
    result = ()
    for model in models:
        inner =  np.array((model.predict(data) - target)**2)
        outer = math.sqrt(np.sum(inner)/target.shape[0])
        result += outer,
    return result

def main(name, target_name = ""):
    words,dates,data = import_csv("../data/" + name + "dat.csv")
    if target_name == "":
        target_name = name
    target_data = get_target_data(target_name)

    for vac, target in target_data:
        print vac
        models = cross_valid(data,target,name)
        res = rmse(models,data,target,name)
        print res









if __name__ == '__main__':
    main("HPV")
    main("PCV","PVC")
    main("DiTe")
    main("MFR","MMR")