#!/usr/bin/python
#-----------------------------------------------------------------------------------------
#This code follows GPL liecense
#
#Author: Abhijit Bendale
#        abendale@uccs.edu
#        Vision and Security Technology lab
#        University of Colorado, Colorado Springs
#
#Date: May 22,2009
#
#Usage: python create_descriptor.py  <list of training images> <path to sift binary>
#This file creates filename.xy, filename.decp file in the caltech 101 directory file 
#filename.xy contains (x,y) location of the keypoint detected by David Lowes SIFT
#filename.decp contains list of geometric blur descriptors around each detected keypoint
#----------------------------------------------------------------------------------------
import sys
import os

from utility_functions import *

trainLst = sys.argv[1]
siftPath = sys.argv[2]

#for each training image:
#    compute sift keypoints
#    get the descriptor around the keypoints
#    save the descriptor at respective location

trainFile = open (trainLst)

for img in trainFile:
    img = img[:-1] #remove new line character
    siftKeys = getKeyPoints(img,siftPath)
    descriptor = getDescriptor(img,siftKeys)
    print len(descriptor)
    descriptorFileName = img[:-3] + 'decp'
    saveDescriptorListFile(descriptor, descriptorFileName)

trainfile.close()
