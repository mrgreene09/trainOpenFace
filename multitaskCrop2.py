#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 09:37:27 2022

@author: joaquintorres
"""
## Use this version when there is already an existing ethnic group folder (with face files) in cropFrames.

# Import libraries
import cv2 
import glob
from mtcnn.mtcnn import MTCNN
import os
import os.path

# Helper functions
## Face detection
def face_detect(img):
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(img)
    return  faces  

# Get input from user about which folder to start
## define where raw frames are
rawFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/'
## define where crops are
cropFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/'

# Automatic cropping of MTCNN detected faces  
ethWhich = input('Which folder would you like to work on? [EX] ')

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