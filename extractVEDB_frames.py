#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 15:22:51 2021

Create a database of VEDB frames sampled every 3 seconds

@author: mgreene2
"""

import os
import cv2
import glob

# root data saving directory
#saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/VEDB_frames/'
saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/pictures'

# get origin root directory
origin = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/videosE1'

# recursively get a list of all directories
#dirs = [x[0] for x in os.walk(origin)]
dirs= os.listdir(path= origin )

# set counters
count = 0



#each name 
name = 'frames'+str(count)

os.mkdir(os.path.join(saveRoot, name))
saveDir = os.path.join(saveRoot, name)

print('Found all directories. Starting to extract frames.')

# loop through each directory
for i in range(len(dirs)):
        
    # see if a world video exists
    if os.path.exists(dirs[i]+'/'+'.mp4'):
        # open the video
        print('Starting folder {}'.format(i))
        
        # make a list of all videos
        videoList = sorted(glob.glob(dirs[i] + '*.mp4'))
        
        # loop through videos
        for v in videoList: 
            
            # create output directory
            videoName = thisPath.split('/')[-1]
            personName= videoName.split ('_') [0]
            personNum = videoName.split('_') [-1]
            Num= personNum[-5]
            person = personName + Num
            
            name = person +str(count)
            if not os.path.exists(os.path.join(saveRoot, name)):
                os.mkdir(os.path.join(saveRoot, name))
                saveDir = os.path.join(saveRoot, name)
            
        
            thisPath = videoList[v]
            vid = cv2.VideoCapture(thisPath)
            
            frameCount = 0
            
            # sample a frame every 3 seconds
            while vid.isOpened():
                # read a frame
                success, image = vid.read()
                frameCount += 1
                
                # assumes that any failure is the end of the video
                if not success:
                    break
                saveName = 'frame'+str(count) # change me
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

