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
#This file contains author written constants that are used in utility_functions.py
#necessary to carry out geometric-blur descriptor based and SVM-KNN implemented 
#object-category recognition system
#---------------------------------------------------------------------------------------

import sys
import ImageFilter

#no of nearest neigbours to be considered
K = 30

circle = {
    #no of radii at which sample points are to be taken 
    #to create geometric blur descriptor
    'ncircs':4,
    #no of sample points per circle
    'nsamples':24,
    #radii in pixel
    'radii':[5,15,25,35]
    }

#Varying levels of blur
blur1 = ImageFilter.Kernel((3, 3),[0.0751,0.1238,0.0751,0.1238,0.2042,0.1238,0.0751,0.1238,0.0751])
blur2 = ImageFilter.Kernel((3, 3),[0.1019,0.1154,0.1019,0.1154,0.1308,0.1154,0.1019,0.1154,0.1019])
blur4 = ImageFilter.Kernel((3, 3),[0.1088,0.1123,0.1088,0.1123,0.1158,0.1123,0.1088,0.1123,0.1088])
blur8 = ImageFilter.Kernel((3, 3),[0.1105,0.1114,0.1105,0.1114,0.1123,0.1114,0.1105,0.1114,0.1105])

blrs_vec = [blur1, blur2, blur4, blur8]

#Sobel filter at various orientation to create sparse signals
#We consider only 4 levels of blur and 4 different channels (sparse signals
sobelx = ImageFilter.Kernel((3, 3),[-1,-2,-1,0,0,0,1,2,1])
sobely = ImageFilter.Kernel((3, 3),[-1,0,1,-2,0,2,-1,0,1])
sobel45 = ImageFilter.Kernel((3, 3),[0,1,2,-1,0,1,-2,-1,0])
sobel135 = ImageFilter.Kernel((3, 3),[0,-1,-2,1,0,-1,2,1,0])

filters_vec = [sobelx, sobely, sobel45, sobel135]

#Data structure to store various channels at varying levels of blur
gb_image = {

    'ch1' : { 'b1':[],
              'b2':[],
              'b3':[],
              'b4':[]
              },
    'ch2' : {'b1':[],
             'b2':[],
             'b3':[],
             'b4':[]
             },
    'ch3' : {'b1':[],
             'b2':[],
             'b3':[],
             'b4':[]
             },
    'ch4' : {'b1':[],
             'b2':[],
             'b3':[],
             'b4':[]
             }
    }

chns = gb_image.keys()
blrs = gb_image['ch1'].keys()

#Data structure to store x and y locations of sample points around the
#keypoint at various radii
xpts = {'r1':[],'r2':[],'r3':[],'r4':[]}
xkeys = xpts.keys()
ypts = {'r1':[],'r2':[],'r3':[],'r4':[]}
ykeys = ypts.keys()
