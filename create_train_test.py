#!/usr/bin/python
#----------------------------------------------------------------------------------------
#Original Author: Nicolas Pinto, MIT (pinto@mit.edu)
#
#Modifier: Abhijit Bendale
#          abendale@uccs.edu
#          Vision and Security Technology lab
#          University of Colorado, Colorado Springs
#
#Date: May 22,2009
#
#Usage: python create_train_test.py <path to caltech 101 directory> <no of training images>
#This file creates train.lst and test.lst in the current directory which are list of training 
#and testing files.
#
#This code is heavily influenced by Niclas Pinto's (MIT) code on V1 model
#For original code license information refer http://pinto.scripts.mit.edu/Main/HomePage
#
#---------------------------------------------------------------------------------------

import sys
import os
import random

EXTENSIONS = ['.png', '.jpg','.pgm']

img_path = sys.argv[1]
img_path = os.path.abspath(img_path)

ntrain = int(sys.argv[2])

if not os.path.isdir(img_path):
        raise ValueError, "%s is not a directory" % (img_path)

tree = os.walk(img_path)
filelist = []
categories = tree.next()[1]    

for root, dirs, files in tree:
        if dirs != []:
            msgs = ["invalid image tree structure:"]
            for d in dirs:
                msgs += ["  "+"/".join([root, d])]
            msg = "\n".join(msgs)
            raise Exception, msg
        filelist += [ root+'/'+f for f in files if os.path.splitext(f)[-1] in EXTENSIONS ]
filelist.sort()    
kwargs = {}
kwargs['filelist'] = filelist

cats = {}
for f in filelist:
    cat = "/".join(f.split('/')[:-1])
    name = f.split('/')[-1]
    if cat not in cats:
        cats[cat] = [name]
    else:
        cats[cat] += [name]
        
# -- Shuffle the images into a new random order
# -- Organize into training and testing sets
filelists_dict = {}
train = {}
test = {}

for cat in cats:
    filelist = cats[cat]
    random.seed()
    random.shuffle(filelist)
    filelist = [ cat + '/' + f for f in filelist ]
    filelists_dict[cat] = filelist
    train[cat] = filelist[0 : ntrain]
    test[cat] = filelist[ntrain+1:]

trfile = open('train.lst','w')
tsfile = open('test.lst','w')
for i in train.keys():
	for j in train[i]:
		trfile.write(j)
		trfile.write("\n")

	for k in test[i]:
		tsfile.write(k)
		tsfile.write("\n")
trfile.close()
tsfile.close()
