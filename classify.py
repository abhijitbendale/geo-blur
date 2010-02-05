#!/usr/bin/python
#----------------------------------------------------------------------------------------
#This code follows GPL liecense
#
#Author: Abhijit Bendale
#        abendale@uccs.edu
#        Vision and Security Technology lab
#        University of Colorado, Colorado Springs
#
#Date: May 22,2009
#
#Usage: python classify.py <list of testing image> <list of training images> <sift binary Path>
#This file creates test.clslbl file with following entries:
#<filename> <category label from Caltech 101> <category label assigned by SVM-KNN>
#---------------------------------------------------------------------------------------

import sys
import os
from utility_functions import *
from PyML import *
from PyML.classifiers import multi

testLst = sys.argv[1]
trainLst = sys.argv[2]
siftPath = sys.argv[3]

resultFile = open("test.clslbl", "w")

testFile = open(testLst,"r")
for query in testFile:
    query = query[:-1]
    print query
    KNN, queryDescriptor = getNeighbours(query , trainLst, siftPath)
    sameClass, sameCat = checkSameClass(KNN)

    if(sameClass):
        resultFile.write(str(query + " " + sameCat + "\n"))
    else:
        #training of SVM
        trainData, trainLabels = getTrainingData(KNN)
        multiSvmTrainData = VectorDataSet(trainData, L = trainLabels)
        mclass = multi.OneAgainstRest (svm.SVM())
        mclass.train(multiSvmTrainData)
        #testing of SVM
        testLabels = []
        lbl = query.split("/")[-2]
        for i in range(len(queryDescriptor)):
            testLabels += [lbl]
        testData = VectorDataSet(queryDescriptor, L = testLabels)
        result = mclass.test(testData)
        predictedLabels = result.getPredictedLabels()
        #check this
        svmCat = max_occuring_cat(predictedLabels)
        
    resultFile.write(str(query + " " + svmCat + "\n"))

testFile.close()       
resultFile.close()
