#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import csv
import codecs
import json

customSplit = u"\t||\t"


def readData(path):
    sent = []
    text = []
    with codecs.open(path,encoding= "utf-8") as f:
        next(f)  # skip headings
        file = f.read()
        file = file.split("\n")
        file = map(lambda x: x.encode("utf-8"),file)
        reader = csv.reader(file,delimiter='\t')
        for _, sen, _, tex, _ in reader:
            if sen in ["-1", "0", "1"]:
                sent.append(int(sen))
                text.append(tex)
    comb = np.column_stack((sent, text))
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



if __name__ == "__main__":
    data = readData("../Data/truth.tsv")
    saveCSV(data,"../Data/truth2.tsv")
    dat = readCustomDat("../Data/truth2.tsv")
    print dat
