#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import string
import re

with open('../sources/stopwords.txt', 'r') as f:
    stop_words = f.read().decode("UTF-8")
    f.close()

stop_words = stop_words.split("\n")

stop_words = list(set(map(lambda x: x.split(" ")[0],stop_words)))

def importFile(path):

    with open(path, 'r') as f:
        file = f.read().decode("UTF-8")
        f.close()
    file = file.lower()
    file = " ".join(filter(lambda x: x not in stop_words,file.split()))
    regex = re.escape(string.punctuation)
    result = re.sub("["+regex+"]"," ",file)
    regex = re.escape(string.whitespace)
    result = re.sub("["+regex+"]+",",",result)
    return result

p1 = importFile("../data/p1.txt").split(",")
p2 = importFile("../data/p2.txt").split(",")
pwords = filter(lambda x: x in p2,p1)
print pwords
