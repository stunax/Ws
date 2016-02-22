#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import re
from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import sys
codec=sys.stdin.encoding

with open('../sources/stopwords.txt', 'r') as f:
    stop_words = f.read().decode("UTF-8")
    f.close()

stop_words = stop_words.split("\n")

stop_words = list(set(map(lambda x: x.split(" ")[0],stop_words)))

def read_file(path):
    with open(path, 'r') as f:
        file = f.read()
        f.close()
    return file


def importFile(path):
    file = read_file(path).decode("utf-8")
    file = file.lower()
    file = " ".join(filter(lambda x: x not in stop_words,file.split()))
    regex = re.escape(string.punctuation)
    result = re.sub("["+regex+"]"," ",file)
    result = re.sub("["+string.whitespace+"]+",",",result)
    return result.encode("utf-8")

def tokenize(path1,path2):
    file1 = importFile(path1).split(",")
    file2 = importFile(path2).split(",")
    words = filter(lambda x: x in file2,file1)
    words = list(set(words))
    words = map(lambda x: x.decode("utf-8"),words)
    return words

def getData(words,name):
    for word in words:
        print "Handling word: " + word
        #Make request
        google.request_report(word, hl='dk', geo="DK", date="01/2010 60m")
        #Get data as csv
        google.save_csv("../data/", name+word)
        time.sleep(randint(2, 10))

print "Talking with google. This takes time!"
google_username = "cmollgaard2"
google_password = "password123!\"#"
google = pyGTrends(google_username, google_password)

getData(["æøå"],"")
pwords = tokenize("../data/p1.txt","../data/p2.txt")
hpvwords = tokenize("../data/HPV1.txt","../data/HPV2.txt")


#getData(pwords,"p")
#getData(hpvwords,"HPV")
