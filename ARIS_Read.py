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
#Rectify method with argument
#Reduce the gain
#populate help function
#Populate doc string
#Post to github
#Export to video

print __doc__

import numpy as np
import matplotlib.pyplot as plt
import pyARIS

#File name
filename = 'C:/Coding_Projects/PyARIS/2013-12-06_132430.aris'

#Open file header and extract metadata
test = pyARIS.DataImport(filename)

#List of attributes
att = dir(test)

#Retreive frame data with metadata
test_frame = pyARIS.FrameRead(test, 1)
frame = test_frame.frame_data


#Expand x axis      
x_factor = 6

for x in range(0,test_frame.BeamCount*x_factor,x_factor):
    for y in range(x_factor-1):
        frame = np.insert(frame, x, frame[:,(x+y)], axis=1)

#Plot
plt.imshow(frame, origin = "lower", vmin = 0, vmax = 80)
plt.show()

#Remap
to = np.array([[1,2],[3,6]])