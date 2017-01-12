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
#Smooth data (i.e. add interpolated beams)
#Reduce the gain
#populate help function
#Populate doc string
#Post to github
#Export to video
#How do we get range and positional measurements? 

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import pyARIS
import beamLookUp

#File name
filename = 'C:/Coding_Projects/PyARIS/2013-12-06_132430.aris'
#filename = 'D:/Programs/Google Drive/PyARIS/2013-12-06_132430.aris'



#Open file header and extract metadata
test = pyARIS.DataImport(filename)

#List of attributes
att = dir(test)

#Retreive frame data with metadata
test_frame = pyARIS.FrameRead(test, 1)

#Remap ARIS Data
pyARIS.createLUP(test, test_frame) #Speed up?
pyARIS.remapARIS(test, test_frame, frameBuffer = 0.05)


#Plot
graphSize = (12, 8)
rcParams['figure.figsize'] = graphSize
plt.imshow(test_frame.remap, origin = "lower", vmin = 0, vmax = 100)
#plt.savefig('frame.png', bbox_inches = 'tight', pad_inches = 0.25)
plt.show()

#List of attributes
att2 = dir(test_frame)

#Expand x axis      
x_factor = 6

for x in range(0,test_frame.BeamCount*x_factor,x_factor):
    for y in range(x_factor-1):
        frame = np.insert(frame, x, frame[:,(x+y)], axis=1)

#Plot
plt.imshow(frame, origin = "lower", vmin = 0, vmax = 80)
plt.show()
