# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 14:50:14 2022

@author: joaquintorres
"""

# Import libraries
import cv2 
import glob
import os
import os.path
import shutil
import numpy as np

# Define input and output folders
## Define where images come from
cropFrames = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/cropFrames/'
## Define where non-faces go to
nonFaces = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/nonFaces/'

# Define which ethnic group folder to start with
ethWhich = input('Which folder would you like to work on? [EX] ')

# Sort video folders in EX
vidList = sorted(glob.glob(os.path.join(cropFrames, ethWhich) + '/*'))

# Create ethnic group folder
ethPath = os.path.join(nonFaces, ethWhich)
os.makedirs(ethPath, exist_ok=True)

# Open each video folder
for i in vidList:
    # Set frame count
    frameCount = 0
    
    # Sort images in video folder 'i'
    imgList = sorted(glob.glob(i + '/*.jpg'))
    
    # Create video folder in nonFaces directory
    vidPath = os.path.join(ethPath, i.split('/')[-1])
    os.makedirs(vidPath, exist_ok=True)

    # Does doneFile.npy exist?
    if os.path.exists(vidPath + '/doneFile.npy'):
        continue
    
    else:
        # Are there existing nonFaces in the folder?
        if len(os.listdir(vidPath)) - 1 == 0:
            # Start from the first cropFrames file
            for j in imgList:
                # Frame count
                frameCount += 1
                
                # Open image
                img = cv2.imread(j)
                cv2.imshow('face', img)
                cv2.waitKey(100)
                cv2.destroyAllWindows()
                
                # Is it a face?
                isFace = input('Is it a face? Press enter if yes, n if no. ')
                if isFace == 'n':
                    # Create new name
                    saveName = 'nonFace' + str(frameCount)
                    # Move file
                    shutil.move(j, vidPath + '/' + saveName + '.jpg')
        
            # Create marker indicating if folder is done        
            done = 'all done'
            np.save(vidPath + '/doneFile.npy', done)
            
        else:
            #Find latest nonFace file created
            currentFiles = sorted(glob.glob(os.path.join(nonFaces, ethWhich, i.split('/')[-1]) + '/*.jpg'))
            latestPath = max(currentFiles, key=os.path.getctime)
            latestFile = latestPath.split('/')[-1]
            startNum = int(latestFile[7:-4])
            newPath = i + '/' + 'face' + str(startNum+1) + '.jpg'
            idx = imgList.index(newPath)
            frameCount = startNum
            
            # Start work from startNum
            for j in range(idx, len(imgList)):
                # Frame count
                frameCount += 1
                
                # Open image
                img = cv2.imread(j)
                cv2.imshow('face', img)
                cv2.waitKey(100)
                cv2.destroyAllWindows()
                
                # Is it a face?
                isFace = input('Is it a face? Press enter if yes, n if no. ')
                if isFace == 'n':
                    # Create new name
                    saveName = 'nonFace' + str(frameCount)
                    # Move file
                    shutil.move(j, vidPath + '/' + saveName + '.jpg')
        
            # Create marker indicating if folder is done        
            done = 'all done'
            np.save(vidPath + '/doneFile.npy', done)
                