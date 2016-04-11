#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import urllib
import string
import re
from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import sys
import numpy as np
from  more_itertools import unique_everseen
codec=sys.stdin.encoding

with codecs.open('../sources/stopwords.txt', "r", "utf-8") as f:
    stop_words = f.read()
    f.close()

stop_words = stop_words.split("\n")

stop_words = list(set(map(lambda x: x.split(" ")[0],stop_words)))

def save_words(name,words):
    with(codecs.open("../data/" + name + ".queries.txt","w+","utf-8")) as f:
        f.write("\r\n".join(words))
        f.close()

def read_file(path):
    with codecs.open(path, "r", "utf-8") as f:
        file = f.read()
        f.close()

    return file
def save_csv(path,data,words,months):
    months = map(lambda x: x.encode("utf-8"),months)
    result = "month," + ",".join(words)
    for i in range(len(months)):
        result += "\n" + months[i]
        for j in range(words.size):
            result += "," + str(data[i,j])
    with codecs.open(path, 'w+', "utf-8") as f:
        f.write(result)
        f.close()
    return  result

def mergedate(dates,times):
    result = []
    current = 0
    currentdate = dates[0]
    for i in range(len(times)):
        if dates[i] != currentdate:
            result.append(current)
            currentdate = dates[i]
            current = 0
        current += times[i]

    return result

def onlymonths(wordfile,months):
    if len(wordfile) == months:
        return map(lambda x:x.split("\n")[0],wordfile)
    splt = map(lambda x: x.split(","),wordfile)
    startdate = map(lambda x: x[0],splt)
    times = map(lambda x: int(x[1]),splt)
    times = mergedate(startdate,times)
    startdate = list(unique_everseen(startdate))
    wordfile = map(lambda x:x[0]+ "," + str(x[1]),zip(startdate,times))


    return wordfile

def importFile(path):
    file = read_file(path)
    file = " ".join(filter(lambda x: x not in stop_words,file.split()))
    regex = re.escape(string.punctuation)
    result = re.sub("["+regex+"0-9]"," ",file)
    result = re.sub("["+string.whitespace+"]+",",",result)
    return result

def tokenize(path1,path2):
    file1 = importFile(path1).split(",")
    file2 = importFile(path2).split(",")
    words = filter(lambda x: x in file2,file1)
    words = list(set(words))
    words = map(lambda x:x.lower(),words)
    return words

def getData(words,name,google):
    monthsnum = 60
    result = np.zeros((monthsnum,len(words)),np.int)
    dont_skip = np.repeat(True,len(words))
    months = ""
    for i,word in enumerate(words):
        urlver = word.encode("utf8")
        print u"Handling word: " + word
        #Make request
        google.request_report( urlver, hl='dk', geo="DK", date="12/2010 "+str(monthsnum+1)+"m")
        #Get data as csv
        google.save_csv("../data/"+name+"/","temp")
        with open("../data/"+name+"/temp.csv") as f:
            wordfile = f.read()
            f.close()
        ## Prepare format
        # find all dates wit report
        wordfile = re.findall("\n([0-9]+-[0-9]+)[0-9 \\-]*,([0-9]+)",wordfile)
        print wordfile
        wordfile = map(lambda x: x[0] + "," + x[1],wordfile)
        if len(wordfile) == 0:
            #If file is empty, don't crash
            dont_skip[i] = False
            continue
        #If weekly data, convert to monthly.
        wordfile = onlymonths(wordfile,monthsnum)
        if len(wordfile) > 0:
            months = wordfile
        wordfilenum = map(lambda x: x.split(",")[1],wordfile)
        result[:,i] = np.array(wordfilenum)
        time.sleep(randint(2, 5))
    words = np.array(words)[dont_skip]
    months = map(lambda x: x.split(",")[0],months)
    result = result[:,dont_skip]
    return (result,words,months)

def main(text1,text2,name,google):
    words = tokenize(text1,text2)
    save_words(name,words)
    data = getData(words,name,google)
    save_csv("../data/" + name + "dat.csv",data[0],data[1],data[2])
    print "done with " + name


if __name__ == '__main__':
    #getData([u"æøå"],"")
    print "Talking with google. This takes time!"
    google_username = "cmollgaard2"
    google_password = "password123!\"#"
    google = pyGTrends(google_username, google_password)
    main("../data/MFR1.txt","../data/MFR2.txt","MFR",google)
    #main("../data/DiTe1.txt","../data/DiTe2.txt","DiTe",google)
    main("../data/HPV1.txt","../data/HPV2.txt","HPV",google)
    #main("../data/PCV1.txt","../data/PCV2.txt","PCV",google)
