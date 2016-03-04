#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import re
from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import sys
import numpy as np
from  more_itertools import unique_everseen
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
def save_csv(path,data,words,months):
    months = map(lambda x: x.encode("utf-8"),months)
    result = "month," + ",".join(words)
    for i in range(len(months)):
        result += "\n" + months[i]
        for j in range(len(data[0])):
            result += "," + str(data[i,j])
    with open(path, 'w+') as f:
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
    result = re.sub("["+regex+"]"," ",file)
    result = re.sub("["+string.whitespace+"]+",",",result)
    return result

def tokenize(path1,path2):
    file1 = importFile(path1).split(",")
    file2 = importFile(path2).split(",")
    words = filter(lambda x: x in file2,file1)
    words = list(set(words))
    words = map(lambda x:x.lower(),words)
    return words

def getData(words,name):
    months = 72
    result = np.empty((months,len(words)),np.int)
    for i,word in enumerate(words):
        print "Handling word: " + word
        #Make request
        google.request_report(word, hl='dk', geo="DK", date="01/2010 "+str(months+1)+"m")
        #Get data as csv
        google.save_csv("../data/"+name+"/","temp")
        with open("../data/"+name+"/temp.csv") as f:
            wordfile = f.read()
            f.close()
        ##Prepare format
        #find all dates wit report
        wordfile = re.findall("\n([0-9]+-[0-9]+)[0-9 \\-]*,([0-9]+)",wordfile)
        wordfile = map(lambda x: x[0] + "," + x[1],wordfile)
        if len(wordfile) == 0:
            #If file is empty, don't crash
            result[i] = 0
            continue
        #If weekly data, convert to monthly.
        wordfile = onlymonths(wordfile,months)
        wordfilenum = map(lambda x: x.split(",")[1],wordfile)
        result[:,i] = np.array(wordfilenum)
        time.sleep(randint(2, 10))
    months = map(lambda x: x.split(",")[0],wordfile)
    return (result,words,months)

def main(text1,text2,name):
    words = tokenize(text1,text2)
    data = getData(words,name)
    save_csv("../data/" + name + "dat.csv",data[0],data[1],data[2])


#getData(["æøå"],"")
#tokenize("../data/PCV1.txt","../data/PCV2.txt")
#tokenize("../data/HPV1.txt","../data/HPV2.txt")
#tokenize("../data/MFR1.txt","../data/MFR2.txt")
#tokenize("../data/DiTe1.txt","../data/DiTe2.txt")

print "Talking with google. This takes time!"
google_username = "cmollgaard2"
google_password = "password123!\"#"
google = pyGTrends(google_username, google_password)

#pdat = getData(pwords,"PVC")
#save_csv("../data/PCVdat.csv",pdat[0],pdat[1],pdat[2])
#hpvdat = getData(hpvwords,"HPV")
#save_csv("../data/HPVdat.csv",hpvdat[0],hpvdat[1],hpvdat[2])
#mfrdat = getData(mfrwords,"MFR")
#save_csv("../data/MFRdat.csv",mfrdat[0],mfrdat[1],mfrdat[2])

if __name__ == '__main__':
    main("../data/MFR1.txt","../data/MFR2.txt","MFR")
    main("../data/DiTe1.txt","../data/DiTe2.txt","DiTe")
    main("../data/HPV1.txt","../data/HPV2.txt","HPV")
    main("../data/PCV1.txt","../data/PCV2.txt","PCV")
