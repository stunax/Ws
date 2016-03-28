#!/usr/bin/python
# -*- coding: utf-8 -*-

from uclassify import uclassify
from readData import *



blocksize = 950
WRITE_API_KEY = "kFyg8MU1UhoD"
READ_API_KEY = "nMjEO52GIOLi"

className = "LegoSentiment"

def analyse(data,i):
    locDat = []
    for s in data[i:i+blocksize]:
        locDat.append(s.encode("utf-8"))
    result = a.classifyKeywords(locDat,"Sentiment","uClassify")
    return  result

def train(data,a):
    a.create(className)
    a.addClass([-1,0,1],className)
    




if __name__ == "__main__":

    a = uclassify()
    a.setWriteApiKey(WRITE_API_KEY)
    a.setReadApiKey(READ_API_KEY)
    data = readCustomDat("../Data/truth2.tsv")
    current = 3*blocksize
    result = analyse(data[:, 1], current)
    save(result, "../Data/sentRes.txt")




