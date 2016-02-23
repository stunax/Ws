#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import re
from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import sys
import numpy as np
reload(sys)

codec=sys.stdin.encoding

with open('../sources/stopwords.txt', 'r') as f:
    stop_words = f.read()
    f.close()

stop_words = stop_words.split("\n")

stop_words = list(set(map(lambda x: x.split(" ")[0],stop_words)))

def read_file(path):
    with open(path, 'r') as f:
        file = f.read()
        f.close()
    return file
def save_csv(path,data):
    return  0


def importFile(path):
    file = read_file(path)
    file = " ".join(filter(lambda x: x not in stop_words,file.split()))
    regex = re.escape(string.punctuation)
    result = re.sub("["+regex+"]"," ",file)
    result = re.sub("["+string.whitespace+"]+",",",result)
    return result

def tokenize(path1,path2):
    file1 = importFile(path1).split(",")
    file2 = importFile(path2).split(",")
    words = filter(lambda x: x in file2,file1)
    words = list(set(words))
    return words

def getData(words,name):
    result = np.empty((len(words),72))
    for i,word in enumerate(words):
        print "Handling word: " + word
        #Make request
        google.request_report(word, hl='dk', geo="DK", date="01/2010 72m")
        #Get data as csv
        google.save_csv("../data/"+name+"/","temp")
        with open("../data/"+name+"/temp.csv") as f:
            wordfile = f.readlines()
            f.close()
        wordfile = wordfile[6:78]
        wordfile = map(lambda x: x.split(",")[1],wordfile)
        result[i] = np.array(wordfile)
        time.sleep(randint(2, 10))
    return (result,words)




#getData(["æøå"],"")
pwords = tokenize("../data/p1.txt","../data/p2.txt")
hpvwords = tokenize("../data/HPV1.txt","../data/HPV2.txt")

print "Talking with google. This takes time!"
google_username = "cmollgaard2"
google_password = "password123!\"#"
google = pyGTrends(google_username, google_password)

pdat = getData(pwords,"p")
hpvdat = getData(hpvwords,"HPV")
print pdat
