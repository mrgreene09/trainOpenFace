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

## Bounding box
def line_select_callback(clk, rls):
    global tl_list
    global br_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))

## Bounding box    
def toggle_selector(event):
    toggle_selector.RS.set_active(True)
    
## Release bbox
def onkeypress(event):
    global tl_list
    global br_list
    if event.key == 'q':
        tl_list = np.array(tl_list[0])
        br_list = np.array(br_list[0])
        x, y, x2, y2 = tl_list[0], tl_list[1], br_list[0], br_list[1]
        crop = img[y:y2, x:x2]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        # Save cropped image
        saveName = 'face'+str(frameCount)
        cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)
        plt.close()

# Get input from user about which folder to start
## define where raw frames are
rawFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/'
## define where crops are
cropFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/'

dirList = sorted(glob.glob(rawFrames+ '*'))

# Loop through each ethnic group folder
for i in dirList:
    vidList = sorted(glob.glob(i + '/' + '*'))
    
    # Loop through each person folder
    for j in vidList:
        imgList = sorted(glob.glob(j + '/' + '*.jpg'))
        
        # Set frame count
        frameCount = 0
        
        # Loop through each image
        for k in imgList:
            frameCount += 1
                
            # Reset values
            tr_list = []
            br_list = []
            
            # extract ethnic group name
            ethnicGroup = i.split('/')[-1] 
            
            # extract face frame name
            prelimName = k.split('/')[-1]
            
            # create image directory
            path = os.path.join(cropFrames, ethnicGroup, j.split('/')[-1])
            os.makedirs(path, exist_ok=True)
            
            # Set file name and save path
            saveName = 'face'+str(frameCount)
            newCrop = os.path.join(path, saveName + '.jpg')
            
            # Does the image file exist already?
            if os.path.isfile(newCrop) == True:
                continue
            else:
                # Open the image
                print('Starting {}'.format(prelimName[:-4]) + ' in {}'.format(j.split('/')[-1]))
                img = cv2.imread(k)
                
                # Detect the face
                faces = face_detect(img) 
                
                if len(faces) > 0:
                    x, y, width, height = (faces[0]['box'])
                    
                    # Crop the face
                    crop = img[y:y+height, x:x+width]
                    
                    # Show cropped image
                    cv2.imshow('cropped', crop)
                    cv2.waitKey(250)
                    cv2.destroyAllWindows()
                    
                    # Save image
                    cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)
                    
                # Temporary
                else:
                    continue
                    
                #else:
                    #if os.path.isfile(newCrop) == True:
                        #continue
                    #else:
                        #fig, ax = plt.subplots(1)
                        #mngr = plt.get_current_fig_manager()
                        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        #ax.imshow(img)
                        
                        #plt.show()
                        
                        #facePresent = input('Is there a face? [y/n]: ')
                        
                        #if facePresent == 'y':
                            # Create bounding box
                            #fig, ax = plt.subplots(1)
                            #mngr = plt.get_current_fig_manager()
                            #ax.imshow(img)
                            
                            #toggle_selector.RS = RectangleSelector(
                                #ax, line_select_callback, 
                                #useblit=True,
                                #button=[1], minspanx=5, minspany=5,
                                #spancoords='pixels', interactive=True
                                #)
                            #bbox = plt.connect('key_press_event', toggle_selector)
                            #key = plt.connect('key_press_event', onkeypress)
                            
                            #plt.show()
                   
            cv2.destroyAllWindows()
