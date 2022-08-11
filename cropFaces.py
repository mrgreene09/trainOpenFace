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
                accept = input('Do you accept this face? ')
                
                if accept == 'y':
                    # Save the frame
                    saveName = 'face'+str(frameCount)
                    cv2.imwrite(os.path.join(path, saveName)+'.jpg', image)
                    
                else:
                    # Show full image
                    # Create bounding box
                    
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
