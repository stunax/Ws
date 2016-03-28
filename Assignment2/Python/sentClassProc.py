#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
from readData import readCustomDat, loadRes


def defineResult(data, cut):
    #resValid = map(lambda x: float(x[1]), data)
    #resOpt = map(lambda x: float(x[2][1][1]), data)
    #dat = np.column_stack((resValid, resOpt))
    result = np.zeros((len(data),), np.int)
    for i in range(len(data)):
        if float(data[i][2][0][1]) >= cut and data[i][2][0][0] == u"positive":
            result[i] = 1
        #if float(data[i][2][1][1]) >= cut:
        if float(data[i][2][1][1]) >= cut:
            if data[i][2][1][0] == u"positive":
                result[i] = 1

            if data[i][2][1][0] == u"negative":
                result[i] = -1
    return result


def optCut(data, truth):
    # Only use data that is available
    localTruth = np.array(map(lambda x: int(x[0]), truth[0:len(data)]))
    init = 0.2
    step = .00025
    rang = np.arange(init, .7, step)
    # Minimize error
    minerror = 99999999
    bestCut = init
    print "Optimizing cuts. May take a while"
    for cut in rang:
        dat = defineResult(data, cut)
        error = np.sum(dat != localTruth)
        if error < minerror:
            bestCut = cut
            minerror = error
    dat = defineResult(data, bestCut)
    errors = np.sum(dat != localTruth)
    print "Best cut was:", bestCut, "with", errors, "errors, out of ", dat.shape[0], "data points. Thats", \
        round(errors / float(dat.shape[0]) * 100,2), "percentage error rate"
    onemisses = np.sum(dat[localTruth == 1] != 1)
    zeromisses = np.sum(dat[localTruth == 0] != 0)
    minonemisses = np.sum(dat[localTruth == -1] != -1)
    print "Positve misses:", onemisses,     "/", np.sum(localTruth == 1)
    print "neutral misses:", zeromisses,    "/", np.sum(localTruth == 0)
    print "negative misses:", minonemisses, "/", np.sum(localTruth == -1)

    #for i in range(30):
    #    print dat[i], truth[i][0]







if __name__ == "__main__":
    realDat = readCustomDat("../Data/truth2.tsv")
    classRes = loadRes("../Data/sentRes.txt")
    proc = optCut(classRes,realDat)
