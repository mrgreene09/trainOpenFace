#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:22:51 2021

Create a database of face frames

@author: mgreene2
"""

import os
import cv2
import glob

# root data saving directory
saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/'

# get origin root directory
origin = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/videos'

# recursively get a list of all directories
dirs = sorted([x[0] for x in os.walk(origin)])

# set directories
name = 'rawFrames'
#os.mkdir(os.path.join(saveRoot, name))
saveDir = os.path.join(saveRoot, name)

print('Found all directories. Starting to extract frames.')

# loop through each "E" directory
#for i in range(1, len(dirs)):
for i in range(9, len(dirs)):
    
    # get video list within directory
    # create a list of videos in each directory
    videoList = sorted(glob.glob(dirs[i] + '/' + '*.mp4'))
    
    # extract ethnic group name
    ethnicGroup = dirs[i].split('/')[-1]
    
    # loop through each video and extract frames
     # loop through each video
    for j in range(51,len(videoList)):
        frameCount = 0
        # extract name of video
        prelimName = videoList[j].split('/')[-1]
        prelimName = prelimName[:-4]
        
        # create picture directory
        path = os.path.join(saveDir, ethnicGroup, prelimName)
        os.makedirs(path)
        
        # open the video
        print('Starting video {}'.format(prelimName))
        thisPath = videoList[j]
        vid = cv2.VideoCapture(thisPath)
        
        # extract each frame
        while vid.isOpened():
             # read a frame
            success, image = vid.read()
            frameCount += 1
            
            # assumes that any failure is the end of the video
            if not success:
                break
            
            # save the frame
            saveName = 'frame'+str(frameCount)
            cv2.imwrite(os.path.join(path, saveName)+'.jpg', image)
    
        # release the video when done
        vid.release()

