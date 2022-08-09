#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 13:41:05 2022

@author: mgreene2
"""

import pandas as pd
import glob
import os

origin = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/'

# recursively get a list of all directories
dirs = sorted([x[0] for x in os.walk(origin)])

# create an empty list of categories and people
categories = []
people = []

# loop through each directory
for i in range(len(dirs)):
    
    # check if this is a leaf directory
    pathLength = dirs[i].split('/')
    if len(pathLength)==10:
        categories.append(dirs[i].split('/')[-2])
        people.append(dirs[i].split('/')[-1])
        
# save to spreadsheet
dict = {'category': categories, 'people': people}
df = pd.DataFrame(dict)

# save the dataframe
df.to_csv('RawFramesToClean2.csv', index=False)