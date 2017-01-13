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
#Export to video
#Tranfer to OpenCV
#Reduce the gain
#populate help function
#Populate doc string
#How do we get range and positional measurements? 

import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import pyARIS
import subprocess as sp

#File name
filename = 'C:/Coding_Projects/PyARIS/2013-12-06_132430.aris'
#filename = 'D:/Programs/Google Drive/PyARIS/2013-12-06_132430.aris'

#Open file header and extract metadata
data, frame = pyARIS.DataImport(filename)

#Retreive frame data with metadata
frame = pyARIS.FrameRead(data, 500)


#Plot
graphSize = (12, 8)
rcParams['figure.figsize'] = graphSize
plt.imshow(frame.remap, origin = "lower", vmin = 0, vmax = 100)
#plt.savefig('frame.png', bbox_inches = 'tight', pad_inches = 0.25)
plt.show()


#Video out
command = ['ffmpeg.exe', '-i', 'test.mp4', '-f', 'image2pipe', '-pix_fmt', 'rgb24', '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)



#List of attributes
att2 = dir(test_frame)


#Plot
plt.imshow(frame, origin = "lower", vmin = 0, vmax = 80)
plt.show()
