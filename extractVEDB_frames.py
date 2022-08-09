#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:22:51 2021

Create a database of face frames

@author: mgreene2
"""

import os
import cv2

# root data saving directory
saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/'

# get origin root directory
origin = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/videos'

# recursively get a list of all directories
dirs = sorted([x[0] for x in os.walk(origin)])

# set counters
count = 0
frameCount = 0
name = 'pictures'
os.mkdir(os.path.join(saveRoot, name))
saveDir = os.path.join(saveRoot, name)

print('Found all directories. Starting to extract frames.')

# loop through each "E" directory
for i in range(len(dirs)):
    
    
        
    # see if a world video exists
    if os.path.exists(dirs[i]+'/'+'flink 1.mp4'):
        # open the video
        print('Starting video {}'.format(i))
        thisPath = dirs[i]+'/'+'flink 1.mp4'
        vid = cv2.VideoCapture(thisPath)
        
        # sample a frame every 3 seconds
        while vid.isOpened():
            # read a frame
            success, image = vid.read()
            frameCount += 1
            
            # assumes that any failure is the end of the video
            if not success:
                break
            if frameCount%90 == 0:
                count += 1
                print('Image count: {}'.format(count))
                # resize the image
                image = cv2.resize(image, (256,256), interpolation=cv2.INTER_AREA)
                saveName = 'frame'+str(count)
                cv2.imwrite(os.path.join(saveDir, saveName)+'.jpg', image)
                
            # make a new subdirectory every 5000 frameCount
            if count%5000 == 0:
                name = 'frames'+str(count)
                if not os.path.exists(os.path.join(saveRoot, name)):
                    os.mkdir(os.path.join(saveRoot, name))
                saveDir = os.path.join(saveRoot, name)
                #count += 1
                
        # release the video when done
        vid.release()

