#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 09:38:32 2022

@author: bcvl
"""
# Import libraries
import cv2 
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import glob

# Global constants
tl_list = []
br_list = []

## Coordinates of bounding box
def line_select_callback(clk, rls):
    global tl_list
    global br_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))

## Drawing bounding box    
def toggle_selector(event):
    toggle_selector.RS.set_active(True)
    
## Release bbox
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
        saveName = 'faceTest' + str(frameCount)
        cv2.imwrite('/Users/bcvl/Desktop/' + saveName + '.jpg', crop)
        plt.close()
        # Reset values for the next image
        tl_list = []
        br_list = []

dirList = '/Volumes/etna/Scholarship/Michelle Greene/Shared/AminaThesis/rawFrames/E9/calinalawrence_E9_A3_flink 1/'

imgList = sorted(glob.glob(dirList + '*.jpg'))

frameCount = 0

for i in imgList:
    frameCount += 1
    img = cv2.imread(i)

    # Open image for assessment
    fig, ax = plt.subplots(1)
    mngr = plt.get_current_fig_manager()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ax.imshow(img)
        
    toggle_selector.RS = RectangleSelector(
        ax, line_select_callback,
        useblit=True,
        button=[1], minspanx=5, minspany=5,
        spancoords='pixels', interactive=True
        )
    bbox = plt.connect('key_press_event', toggle_selector)
    key = plt.connect('key_press_event', onkeypress)
    plt.show()