#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:17:09 2022

@author: bcvl
"""
# Import libraries
import cv2 
import glob
from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os
import os.path

# Global constants
tl_list = []
br_list = []

# Helper functions
## Face detection
def face_detect(img):
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(img)
    return  faces  

## Save coordinates of bounding box
def line_select_callback(clk, rls):
    global tl_list
    global br_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))

## Draw bounding box 
def toggle_selector(event):
    toggle_selector.RS.set_active(True)
    
## Release bbox and save crop
def onkeypress(event):
    global tl_list
    global br_list
    if event.key == 'q':
        # Save coordinates
        x, y, x2, y2 = tl_list[0][0], tl_list[0][1], br_list[0][0], br_list[0][1]
        # Crop image
        crop = img[y:y2, x:x2]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        # Save cropped image
        cv2.imwrite(newCrop, crop)
        plt.close()
        # Reset values for the next image
        tl_list = []
        br_list = []

# Get input from user about which folder to start
## define where raw frames are
rawFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/'
## define where crops are
cropFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/'

cropTask = input('Choose [automate/manual/postclean]: ')

# Manual cropping of faces not detected by MTCNN, including for postclean (run it again after)
if cropTask == 'manual':
    # Sort ethnic group folders
    dirList = sorted(glob.glob(rawFrames+ '*/'))
    
    for i in dirList:
        # extract ethnic group name
        ethnicGroup = i.split('/')[-2]
        
        ethWhich = input('Which folder would you like to work on? [EX] ')
        
        if ethWhich == ethnicGroup:
            # Sort video folders
            vidList = sorted(glob.glob(os.path.join(rawFrames, ethWhich + '/*')))
            
            # Create path of each ethnic group folder in cropFrames
            cropVidList = os.path.join(cropFrames, ethnicGroup + '/')
            
            for j in vidList:
                # Sort image folders
                imgList = sorted(glob.glob(j + '/*'))
                
                # Set frame count
                frameCount = 0
                
                # Create path of each video folder in cropFrames
                vidName = j.split('/')[-1]
                vidDir = os.path.join(cropVidList, vidName)
                os.makedirs(vidDir, exist_ok=True)
                
                for k in imgList:
                    frameCount += 1
                    
                    # extract face frame name
                    prelimName = k.split('/')[-1]
                    
                    # Set path and file name for each image file
                    saveName = 'face'+str(frameCount)
                    newCrop = os.path.join(vidDir, saveName + '.jpg')
                    
                    if os.path.isfile(newCrop) == True:
                        continue # Skip existing files
                    else:
                        # Open the image
                        print('Working on {}'.format(prelimName[:-4]) + ' in {}'.format(j.split('/')[-1]))
                        img = cv2.imread(k)
                        
                        # Open image for assessment
                        fig, ax = plt.subplots(1)
                        mngr = plt.get_current_fig_manager()
                        ax.imshow(img)
                        
                        # Create bounding box
                        toggle_selector.RS = RectangleSelector(
                            ax, line_select_callback, 
                            useblit=True,
                            button=[1], minspanx=5, minspany=5,
                            spancoords='pixels', interactive=True
                            )
                        bbox = plt.connect('key_press_event', toggle_selector)
                        key = plt.connect('key_press_event', onkeypress)
                        
                        plt.show()
                        
                        print('Saved as {}'.format(saveName))