#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:14:42 2023

Compiles all parts of the cropFaces process to crop face frames more efficiently

@author: joaquinmtorres
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

cropTask = input('Choose [automate/manual]: ')

# Automatic cropping of MTCNN detected faces
if cropTask == 'automate':    
    # Determine which ethnic group folder to work on
    ethWhich = input('Which folder would you like to work on? [EX] ')
    
    # Compare ethnic group folders in rawFrames and cropFrames directories
    if len(os.listdir(rawFrames)) == len(os.listdir(cropFrames)):
        print('Automate task finished.')
        
    else:
        # Choose ethnic group folder
        ethWhich = input('Which folder would you like to work on? [EX] ')
        
        dirList = sorted(glob.glob(os.path.join(rawFrames, ethWhich) + '/*')) # Sorts all video folders in ethWhich
        
        # If there are no existing JPEG files in ethWhich (i.e. you're starting on a new ethnic group folder)
        ethPath = sorted(glob.glob(os.path.join(cropFrames, ethWhich) + '/*/*.jpg'))
        if len(ethPath) == 0:
            for i in dirList:  
                # sort image folders
                imgList = sorted(glob.glob(i + '/*.jpg'))
                    
                # Create path of each ethnic group folder in cropFrames
                cropVidList = os.path.join(cropFrames, ethWhich + '/')
                
                # Set frame count
                frameCount = 0
                
                # Loop through each image in video folder
                for j in imgList:
                    frameCount += 1
                    
                    # Create path of each video folder in cropFrames
                    vidName = j.split('/')[-2]
                    vidDir = os.path.join(cropVidList, vidName)
                    
                    # create image directory
                    path = os.path.join(cropFrames, ethWhich, vidName)
                    os.makedirs(path, exist_ok=True)
                    
                    # extract face frame name
                    prelimName = j.split('/')[-1]
                    
                    # Set file name and save path
                    saveName = 'face'+str(frameCount)
                    newCrop = os.path.join(path, saveName + '.jpg')
                    
                    # Skip existing files
                    if os.path.isfile(newCrop) == True:
                        continue
                    
                    else:
                        # Open the image
                        print('Starting {}'.format(prelimName[:-4]) + ' in {}'.format(j.split('/')[-2]))
                        img = cv2.imread(j)
                        
                        # Detect the face
                        faces = face_detect(img) 
                        
                        # MTCNN detects a face
                        if len(faces) > 0:
                            x, y, width, height = (faces[0]['box'])
                            
                            # Crop the face
                            crop = img[y:y+height, x:x+width]
                            
                            # Show cropped image
                            cv2.imshow('cropped', crop)
                            cv2.waitKey(100)
                            cv2.destroyAllWindows()
                            
                            # Save image
                            cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)                          
                        else:
                            continue 
        
        # If there are existing JPEG files in ethWhich (i.e. you've worked on ethWhich before)
        else:
            # Figure out what the latest file created is
            currentFiles = sorted(glob.glob(os.path.join(cropFrames, ethWhich) + '/*/*.jpg'))
            latestPath = max(currentFiles, key=os.path.getctime)
            latestVid = latestPath.split('/')[-2]

            # Start work on what comes after latestFile
            dirList = sorted(glob.glob(os.path.join(rawFrames, ethWhich) + '/*')) # Sorts all video folders
            # Create start folder
            startFolder = os.path.join(rawFrames, ethWhich, latestVid)
            # Determine index of startFolder
            idx = dirList.index(startFolder)

            for i in range(idx, len(dirList)):  
                # sort image folders
                imgList = sorted(glob.glob(dirList[i] + '/*.jpg'))
                    
                # Create path of each ethnic group folder in cropFrames
                cropVidList = os.path.join(cropFrames, ethWhich + '/')
                
                # Set frame count
                frameCount = 0
                
                # Loop through each image in video folder
                for j in imgList:
                    frameCount += 1
                    
                    # Create path of each video folder in cropFrames
                    vidName = j.split('/')[-2]
                    vidDir = os.path.join(cropVidList, vidName)
                    
                    # create image directory
                    path = os.path.join(cropFrames, ethWhich, vidName)
                    os.makedirs(path, exist_ok=True)
                    
                    # extract face frame name
                    prelimName = j.split('/')[-1]
                    
                    # Set file name and save path
                    saveName = 'face'+str(frameCount)
                    newCrop = os.path.join(path, saveName + '.jpg')
                    
                    # Skip existing files
                    if os.path.isfile(newCrop) == True:
                        continue
                    
                    else:
                        # Open the image
                        print('Starting {}'.format(prelimName[:-4]) + ' in {}'.format(j.split('/')[-2]))
                        img = cv2.imread(j)
                        
                        # Detect the face
                        faces = face_detect(img) 
                        
                        # MTCNN detects a face
                        if len(faces) > 0:
                            x, y, width, height = (faces[0]['box'])
                            
                            # Crop the face
                            crop = img[y:y+height, x:x+width]
                            
                            # Show cropped image
                            cv2.imshow('cropped', crop)
                            cv2.waitKey(100)
                            cv2.destroyAllWindows()
                            
                            # Save image
                            cv2.imwrite(os.path.join(path, saveName)+'.jpg', crop)                          
                        else:
                            continue             

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
                   
else:
    print('Invalid response. Exit program and start again.')