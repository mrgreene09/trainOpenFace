#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 10:28:49 2022

@author: michellegreene
"""

# Import libraries
import cv2 
import glob
from mtcnn.mtcnn import MTCNN
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os

## Global constants
## img = None
## tl_list = []
## br_list = []
## object_list = []

# Helper functions
def face_detect(img):
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(img)
    return  faces  

## def line_select_callback(clk, rls):
    ## gglobal tl_list
    ## global br_list
    ## global object_list
    ## tl_list.append((int(clk.xdata), int(clk.ydata)))
    ## br_list.append((int(rls.xdata), int(rls.ydata)))
    ## object_list.append(obj)
    
## def toggle_selector(event):
    ## toggle_selector.RS.set_active(True)

# Get input from user about which folder to start
## define where raw frames are
rawFrames = "/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/"
## define where crops are
cropFrames = "/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/"

dirList = sorted(glob.glob(rawFrames+ '*'))

# Loop through each folder beginning with start folder
for i in dirList:
    ethList = sorted(glob.glob(i + "/" + "*"))
    
    # Loop through all ethnic group folders
    for j in ethList:
        videoList = sorted(glob.glob(j + "/" + "*"))
        
        # Loop through all video folders
        for k in videoList:
            imageList = sorted(glob.glob(k + "/" + "*.jpg"))

            # Loop through each image
            frameCount = 0
            for l in imageList:
                frameCount += 1
                
                # extract ethnic group name
                ethnicGroup = i.split('/')[-1] 
                
                # extract face frame name
                prelimName = imageList[l].split('/')[-1]
                
                # create image directory
                path = os.path.join(cropFrames, ethnicGroup, prelimName)
                os.makedirs(path)
                
                # Open the image
                img = cv2.imread(l)
                
                # Detect the face
                faces = face_detect(img)  
                x, y, width, height = (faces[0]['box'])
                
                # Crop the face
                crop = img[y:y+height, x:x+width]
                
                # Show cropped image
                cv2.imshow("cropped", crop)
                cv2.waitKey(0) # waiting for any button to be pressed
            
                # Do we accept the face? y/n
                accept = input('Do you accept this face? [y/n]: ')
                
                if accept == 'y':
                    # Save the frame
                    saveName = 'face'+str(frameCount)
                    cv2.imwrite(os.path.join(path, saveName)+'.jpg', img)
                    
                else:
                    # Show full image
                    ## ax.imshow(img)
                    
                    # Create bounding box
                    ## toggle_selector.RS = RectangleSelector(
                        ## ax, line_select_callback,
                        ## drawtype='box', useblit=True,
                        ## button=[1], minspanx=5, minspany=5,
                        ## spancoords='pixels', interactive=True
                    ## )
                    ## bbox = plt.connect('key_press_event', toggle_selector)
                    ## plt.show()
                    
                    # if bbox > 1 pixel:
                        # Crop bounding box image
                        # Save cropped image
                        
                    # else:
                        # next image

                cv2.destroyAllWindows()

# if face detected:
    # Show the cropped face
        # Person says y or n
        # If yes:
            # Saved the cropped image
        # If no:
            # Show full image
            # Person provides bounding box or clicks anywhere one time
            # If bbox > 1 pixel:
                # Save cropped image
            
# else:
    # Show full image
    # Person provides bounding box or clicks anywhere one time
    # If bbox > 1 pixel:
        # Save cropped image
