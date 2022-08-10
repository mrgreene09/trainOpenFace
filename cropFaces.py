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

# Helper functions
def face_detect(img):
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(img)
    return  faces  

# this is a test
# Get input from user about which folder to start
## define where raw frames are
rawFrames = "/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/"
## define where crops are
cropFrames = "/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/"

dirList = sorted(glob.glob(rawFrames+ '*'))

# Loop through each folder beginning with start folder
for i in dirList:
    ethList = sorted(glob.glob(i + "/" + "*"))
# Loop through all video folders
    for j in ethList:
        imageList = sorted(glob.glob(j + "/" + "*.jpg"))
# Loop through each image
        for k in imageList:
            # Open the image
            img = cv2.imread(k)
            # Detect the face
            face_detect(img)            

# Crop the face

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
