#!/bin/bash
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
#This shell script invokes David Lowe's SIFT binary and reformats the file so as to have only
#(x,y) locations of the keypoint detected in <filename>.xy file
#---------------------------------------------------------------------------------------

file=$1
sift=$2
#sift='/home/abendale/Python/geoblur/siftDemoV4/sift'
base=`echo $file | cut -d . -f 1`

mogrify -format pgm ${file}
${sift} < ${base}.pgm > ${base}.key

cat ${base}.key | sed -n 2~8p > ${base}.xyot
cat ${base}.xyot | awk '{print $1,$2;}' > ${base}.xy
rm ${base}.key ${base}.xyot