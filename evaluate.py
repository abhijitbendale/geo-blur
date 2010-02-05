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
#Usage: python classify.py <test.clslbl>
#This file accepts test.clslbl file and creates mean rec_rate.txt file which contains
#recognition rate per object category
#---------------------------------------------------------------------------------------

import sys
import os

labelFile = sys_argv[1]

file = open(labelFile,"r")

for line in file:
    svmCat = line.split(" ")[-1]
    imageCat = line.split(" ")[-2]
    imageCat = imageCat.split("/")[-2]
    
