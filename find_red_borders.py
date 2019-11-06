#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QC script to read video file and search for red borders.
Saves png file with TC for each red border catch.
Iddo Lahman, Bootke color, iddolahman@gmail.com
'''

# ----/user inputs\----

# choose FPS
FPS = 25

# ---------------------

import sys
import os
import cv2
import time as t
import numpy as np
from tkinter import Tk, filedialog

# =-=-=-=-=-=-=-= Utils =-=-=-=-=-=-=-=-=-=
def frames2tc (frames, FPS):
    """
    converts numerical frame count to string representation timecode.
    """
    h = str(int(frames / (FPS * 3600)))
    m = str(int(frames / (FPS * 60)) % 60)
    s = str(int((frames % (FPS * 60)) /FPS))
    f = str(int(frames % (FPS * 60)) % FPS)
    return f'{h.zfill(2)}-{m.zfill(2)}-{s.zfill(2)}-{f.zfill(2)}'

def saveImage(frame, pos, folder):
    """
    creates png file.
    """
    x = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    name = pos +  '_' + frames2tc(x, FPS) + '.png'
    # filename = "{}/{}-Frame_{}.png".format(folder, pos, tc)
    path = outputFolder
    filename = os.path.join(path, name)
    cv2.imwrite(filename, frame)
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# file dialog to ask the user to choose a file.
Tk().withdraw()
inputFile = filedialog.askopenfilename(title='Choose a file', initialdir=os.getcwd())
if not inputFile:     # In case user select "Cancel"
    sys.exit(0)

# file dialog to ask the user to choose output folder.
outputFolder = filedialog.askdirectory(title='Choose output folder', initialdir=os.getcwd())
if not outputFolder:     # In case user select "Cancel"
    sys.exit(0)


cap = cv2.VideoCapture(inputFile)
if not cap.isOpened():
    print('[-] Error:       Could not open file.')
    exit(-1)

start_time = t.time()
print('Reading File...')

while(1):
    ret, frame = cap.read()
    if not ret:
        print('End Of Video')
        break

    height, width, ch = frame.shape

    if int(frame[0,0][2]) - int(frame[0,0][0]) + int(frame[0,0][1]) > 210:
        top = [int(frame[0,x][2]) - int(frame[0,x][1] + frame[0,x][0]) for x in range(width)]
        if np.mean(top) > 228:
            saveImage(frame, 'Top', outputFolder)
        else:
            left = [int(frame[y,0][2]) - int(frame[y,0][1] + frame[y,0][0]) for y in range(height)]
            if np.mean(left) > 228:
                saveImage(frame, 'Left', outputFolder)

    elif int(frame[height-1,width-1][2]) - int(frame[height-1,width-1][1] + frame[height-1,width-1][0]) > 210:
        bottom = [int(frame[height-1, x][2]) - int(frame[height-1, x][1]) + int(frame[height-1, x][0]) for x in range(width)]
        if np.mean(bottom) > 228:
            saveImage(frame, 'Bottom', outputFolder)
        else:
            right = [int(frame[y, width-1][2]) - int(frame[y, width-1][1] + frame[y, width-1][0]) for y in range(height)]
            if np.mean(right) > 228:
                saveImage(frame, 'Right', outputFolder)

cap.release()
cv2.destroyAllWindows()
print('\n---Finished in: {} seconds ---'.format(int(t.time() - start_time)))
