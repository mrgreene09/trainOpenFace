#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 08:11:32 2022

Save all frames from Amina's videos

@author: michellegreene
"""

import os
import cv2
import glob
import pandas as pd

# root data saving directory
#saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/VEDB_frames/'
#saveRoot = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/pictures/'
#saveRoot = '/Volumes/GoogleDrive/Shared drives/Amina Thesis Videos/pictures/'

# get origin root directory
origin = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/videos/'

# recursively get a list of all directories
dirs = [x[0] for x in os.walk(origin)]

# start list for ethnic groups
eGroup = []

# start list for frames
frameList = []

# loop through each directory
for i in range(1, len(dirs)):
#for i in range(1,2):
    # create a list of videos in each directory
    videoList = sorted(glob.glob(dirs[i] + '/' + '*.mp4'))
    
    # extract ethnic group name
    ethnicGroup = dirs[i].split('/')[-1]
    
    # loop through each video
    for j in range(len(videoList)):
        # extract name of video
        prelimName = videoList[j].split('/')[-1]
        prelimName = prelimName[:-4]
        
        # open the video
        print('Starting video {}'.format(prelimName))
        thisPath = videoList[j]
        vid = cv2.VideoCapture(thisPath)
        #frame = 0
        
        # get the number of frames
        frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        
        # save ethinic group and frames
        eGroup.append(ethnicGroup)
        frameList.append(frames)
        
        # create picture directory
        #path = os.path.join(saveRoot, ethnicGroup, prelimName)
        #os.makedirs(path)
        
        # # extract each frame
        # while vid.isOpened():
        #     # read a frame
        #     success, image = vid.read()
            
        #     # assumes that any failure is the end of the video
        #     if not success:
        #         break
            
        #     frame += 1
        #     saveName = 'frame'+str(frame)+'.jpg'
        #     cv2.imwrite(path+'/'+saveName, image)
            
        vid.release()
        
# save to csv
d = {'Ethnic Group': eGroup, 'FrameCount': frameList}
df = pd.DataFrame(data=d)
df.to_csv('frameCounts.csv', index=False)
        