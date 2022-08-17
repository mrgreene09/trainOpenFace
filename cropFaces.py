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
        crop = img[x:x2, y:y2]
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        # Save cropped image
        saveName = 'face'+str(frameCount)
        cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)
        plt.close()

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
        #folderList = sorted(glob.glob(j + "/" + "*"))
        folderList = os.listdir(i)
        
        # Loop through all video folders
        for k in folderList:
            thisPath = os.path.join(i, k)
            #imageList = sorted(glob.glob(k + "/" + "*.jpg"))
            imageList = sorted(glob.glob(thisPath + '/*.jpg'))

            # Loop through each image
            frameCount = 0
            for l in imageList:
                frameCount += 1
                
                # extract ethnic group name
                ethnicGroup = i.split('/')[-1] 
                
                # extract face frame name
                prelimName = l.split('/')[-1]
                prelimName = prelimName[:-4]
                
                # create image directory
                try:
                    path = os.path.join(cropFrames, ethnicGroup, k)
                    os.makedirs(path)
                except:
                    continue
                
                # Open the image
                print('Starting {}'.format(prelimName) + ' in {}'.format(k))
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
                
                cv2.destroyAllWindows()

                if accept == 'y':
                    # Save the frame
                    saveName = 'face'+str(frameCount)
                    cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)
                    
                else:
                    fig, ax = plt.subplots(1)
                    mngr = plt.get_current_fig_manager()
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    ax.imshow(img)

                    plt.show()

                    facePresent = input('Is there a face? [y/n]: ')

                    if facePresent == 'y':
                        # cv2.destroyAllWindows
                        # Create bounding box
                        fig, ax = plt.subplots(1)
                        mngr = plt.get_current_fig_manager()
                        ax.imshow(img)
                        
                        toggle_selector.RS = RectangleSelector(
                            ax, line_select_callback,
                            #drawtype='box', 
                            useblit=True,
                            button=[1], minspanx=5, minspany=5,
                            spancoords='pixels', interactive=True
                            )
                        bbox = plt.connect('key_press_event', toggle_selector)
                        key = plt.connect('key_press_event', onkeypress)
                        
                        plt.show()
                       
                cv2.destroyAllWindows()