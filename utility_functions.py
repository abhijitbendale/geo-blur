#!/usr/bin/python
#
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
#This file contains all author written functions necessary to carry out geometric-blur
#descriptor based and SVM-KNN implemented object-category recognition system
#---------------------------------------------------------------------------------------

import sys
import os
import pickle
import math
import Image
import ImageOps
import ImageFilter

from operator import itemgetter

from gb_params import *

#Given an image file path, this function returns the list of keypoint (x,y) locations
#This functions calls Davis Lowe's SIFT binary for keypoint detection via sift.sh
def getKeyPoints (filename,siftPath):
    #Find Keypoints for a given image
    siftBinary = '/home/abendale/Geoblur/sift.sh ' + filename + " " + siftPath 
    os.system(siftBinary)
    
#    os.system('/home/abendale/Geoblur/sift.sh ' + filename) 
    
    #Read x,y of the keypoint
    keyfile = filename.replace(".jpg",".xy") 
    print keyfile

    siftKeys = []
    xyFile = open(keyfile,'r')

    for line in xyFile:
        line = line[:-1]
        tmp = line.split(" ")
        siftKeys += [tmp]
            
    xyFile.close()
    
    return siftKeys

#checks if for given keypoint, if all the sampled pixels for largest blur radii
#lie within the boundary of image
def inBounds(x,y,iw,ih,increamentAngle):

    bounds = 0

    r = max(circle['radii'])

    for theta in range(0,360,increamentAngle):
        x_circ = x + r * math.cos((theta * math.pi)/180)
        if x_circ < 0 or x_circ > iw - 4:
            return False 

        y_circ = y - r * math.sin((theta * math.pi)/180)
        if y_circ < 0 or y_circ > ih - 4:
            return False 
      
    return True
    
#for a given image with list of keypoint location, this function computes the
#geometric blur descriptor and returns the list of descriptors around all the 
#keypoints of the image
def getDescriptor (fileName, siftKeys):   
    #fileName = fileName[:-1]
    img = Image.open(fileName)
    img = ImageOps.grayscale(img)
    iw,ih = img.size

    #Create sample points at 15 degrees on a circle
    increamentAngle = 360/circle['nsamples']
    gb_descriptor = []
        
    for kpt in range(0,len(siftKeys)):#for each keypoint
        x = math.floor(float(siftKeys[kpt][0]))
        y = math.floor(float(siftKeys[kpt][1]))

        if ( inBounds (x,y,iw,ih,increamentAngle) ):

            #Calculate the pixel locations around the keypoint at which sparse signals will
	    #be extracted to for geometric blur descriptor
            for i in range(len(circle['radii'])):
                r = circle['radii'][i]
                xpts[xkeys[i]] = [math.floor(x + r * math.cos((theta * math.pi)/180)) for theta in range(0,360,increamentAngle)]
                ypts[ykeys[i]] = [math.floor(y - r * math.sin((theta * math.pi)/180)) for theta in range(0,360,increamentAngle)]

            #Generate sobel based filters (sparse signals from the image)
            for i in range(4):
                ch = img.filter(filters_vec[i]) #Create sobel based sparse channels for each image
                for j in range(4):
                    gb_image[ chns[i] ][ blrs[j] ] = ch.filter( blrs_vec[j] ) #Blur each channel with varying sigma
                    
            descriptor = []
            descriptor += [x]
            descriptor += [y]

            for i in gb_image.keys():
                for j in range(4):
                    descriptor += [ gb_image[i][blrs[j]].getpixel((xpts[xkeys[j]][k],ypts[ykeys[j]][k])) for k in range(24) ]

            gb_descriptor.append(descriptor)
    return gb_descriptor

def saveDescriptorListFile(descriptor, descriptorFilename):
    file = open(descriptorFilename,"w")
    pickle.dump(descriptor, file)
    file.close()    

def readDescriptorListFile(descriptorFilename):
    file = open(descriptorFilename,"r")
    descriptorList = pickle.load(file)
    return descriptorList

#Computes accurate distance between two images as defined in SVM-KNN
#paper Section 4.4, Algorithm B
def accurateDistance(A,B):
    
    lamda = 0.25  
    r0 = 270 #avg image size of Caltech 101
    oneWayDistance = 0

    for i in range(len(A)):
        A_x = A[i][0]
        A_y = A[i][1]
        descriptorI = A[i][2:]
        featureDistance = []

        for j in range (len(B)):
            B_x = B[j][0]
            B_y = B[j][1]
            descriptorJ = B[j][2:]
            tmpDist = 0
            for k in range (len(descriptorJ)):
                tmpDist = tmpDist + (descriptorI[k] - descriptorJ[k])

            featureDistance +=[ (tmpDist)**2 + (lamda/r0)*(abs(A_x - B_x) + abs(A_y - B_y)) ]

        oneWayDistance = oneWayDistance + min(featureDistance)
    return oneWayDistance/len(A)

#For a given query image, this function returns list of K (here K = 30)
#neighbours
def getNeighbours(queryImage, trainLst, siftPath):
    querySiftKeys = getKeyPoints(queryImage, siftPath)
    queryDescriptor = getDescriptor(queryImage, querySiftKeys)
    distanceArray = []
    distanceImage = []

    trainFile = open(trainLst,"r")

    for image in trainFile:
        imageDescriptorFile = image[:-4]  + 'decp'
        imageDescriptor = readDescriptorListFile (imageDescriptorFile)
        distanceArray += [accurateDistance(queryDescriptor, imageDescriptor) + accurateDistance(imageDescriptor, queryDescriptor)]
        distanceImage += [image]

    trainFile.close()
    #Sort by distance and get Neartest neighbours
    allNeighbours = dict(zip(distanceArray, distanceImage))
    items = allNeighbours.items()
    items.sort(key = itemgetter(1))
    
    KNNs = []
    for i in items[:K]:
        KNNs += [i[0]]
    
    return KNNs, queryDescriptor

#Given a list of K neighbours, the function checks if all the 
#neighbours belong to the same class
def checkSameClass(KNN):
    cats = []
    cats[0] = [KNN[0].split("/")[-2]]
    NN = KNN[1:]
    i = 0

    for image in NN:
        cat += [image.split("/")[-2]]
        i = i + 1
        if cat[0] != cat[i]:
            return False, cat

    return True,cat

#This function attaches category label to each descriptor for each
#of the K - Nearest Neighbours
def getTrainingData(KNN):
    multiData = []

    for neighbour in KNN:
        data = readDescriptorFromFile(neighbour)
        cat = neighbour.split('/')[-2]
        for i in data:
            i.append(cat)
        multiData += [data]

    return multiData

