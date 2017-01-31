# -*- coding: utf-8 -*-
"""
===================================================
Read ARIS files into python
===================================================

Developed by Chris Rillahan 
Last Modified: December 20, 2016

This 

"""

#ToDo
#Reduce the gain
#Populate doc string
#Add some error trapping
#How do we get range and positional measurements? 
#Speed up translation
#Smooth images
#Add timestamp to video output? Histogram equalization?#Add other resolution modes
#Check dependencies

#import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import pyARIS
from PIL import Image
import cv2

#File name
filename = 'C:/Coding_Projects/PyARIS/2013-12-06_132430.aris'
#filename = 'D:/Programs/Google Drive/PyARIS/2013-12-06_132430.aris'

#Open file header and extract metadata
data, frame = pyARIS.DataImport(filename)

#Retreive frame data with metadata
frame = pyARIS.FrameRead(data, 1)

#Output image vis PIL
im = Image.fromarray(frame.remap)
im.show()

#Show via openCV
cv2.imshow('data',frame.remap)
cv2.waitKey(5000)
cv2.destroyAllWindows()

#Plot with matplotlib
graphSize = (12, 8)
rcParams['figure.figsize'] = graphSize
plt.imshow(frame.remap, origin = "lower", vmin = 0, vmax = 255)
plt.savefig('frame.png', bbox_inches = 'tight', pad_inches = 0.25)
plt.show()


#Video out	
pyARIS.VideoExport(data, 'test_video.mp4', end_frame = 50)