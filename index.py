#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.2.0),
    on 十一月 30, 2022, at 22:55
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding
import re
import pandas as pd

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.0'
expName = 'VBDM'  # from the Builder filename that created this script
expInfo = {'participant': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr(format = "%Y-%m-%d-%H%M")  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExpRating = data.ExperimentHandler(name=expName+'_Rating', version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=False, saveWideText=True,
    dataFileName=filename+'_Rating')

thisExpChoice = data.ExperimentHandler(name=expName+'_Choice', version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=False, saveWideText=True,
    dataFileName=filename+'_Choice')

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None


# Start Code - component code to be run after the window creation
from ratingRoutines.components import * 
from ratingRoutines.ratings import singleImage
from ratingRoutines.vbdmRound import *
from ratingRoutines.makeStim import makeStim

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

###########################################################

StartInterface()

faceList = os.listdir('Face Choose')
faceList = sorted(faceList, key=lambda x: int(re.search('\d+', x)[0]))
np.random.shuffle(faceList)
# print(faceList)
for img in faceList[:10]:
    singleImage(thisExpRating, img)

thisExpRating.saveAsWideText(filename+'_RatingBackup'+'.csv', delim='auto')
print('filename:', filename+'_RatingBackup'+'.csv') # 不用這個會找不到檔案

###########################################################
Rating = pd.read_csv(filename+'_RatingBackup'+'.csv')
# print(Rating)
# Rating = pd.read_csv('data/1_Rating_2022-12-25-1438_Rating.csv')
Rating = Rating.sort_values('Name', key=lambda x: sorted(x.str.slice(start=2, stop=-4)))
Rating.loc[Rating.query('rating==10').index, 'rating'] = 9
ratings_counts=Rating['rating'].value_counts()
print('ratings_counts', ratings_counts)
allcounts = [ratings_counts[i] for i in range(5,10)]
temp = [list(np.repeat(i+5, count)) for i, count in enumerate(allcounts)]
ratings = [[str(level)+'_'+str(ind+1) for ind,level in enumerate(levelList)] for levelList in temp]
stimDict = {}
for i, level in enumerate(ratings):
    iterator = iter(list(Rating[Rating['rating'] == i+5]['Name']))
    for key in level:
        stimDict[key] = next(iterator)

stimList1, stimList2 = makeStim(allcounts)
stimList1_All = [stim for diffList in stimList1 for stim in diffList]
np.random.shuffle(stimList1_All)
stimList2_All = [stim for diffList in stimList2 for stim in diffList]
np.random.shuffle(stimList2_All)

##########################################################
isPressureFirst = bool(int(expInfo['participant'])%2)
if isPressureFirst:
    instructionImg = './ratingRoutines/Pressure.png'
else:
    instructionImg = './ratingRoutines/noPressure.png'

InstructionInterface(instructionImg)
for stim in stimList1_All:
    difficulty = abs(int(stim[1].split('_')[0])-int(stim[0].split('_')[0]))
    leftInd = np.random.randint(2)
    rightInd = abs(leftInd-1)
    left = stimDict[stim[leftInd]]
    right = stimDict[stim[rightInd]]
    VBDM(thisExpChoice, right, left, difficulty, isPressureFirst)
    Interval(2)

########################################################
if not isPressureFirst:
    instructionImg = './ratingRoutines/Pressure.png'
else:
    instructionImg = './ratingRoutines/noPressure.png'

InstructionInterface(instructionImg)
for stim in stimList2_All:
    difficulty = abs(int(stim[1].split('_')[0])-int(stim[0].split('_')[0]))
    leftInd = np.random.randint(2)
    rightInd = abs(leftInd-1)
    left = stimDict[stim[leftInd]]
    right = stimDict[stim[rightInd]]
    VBDM(thisExpChoice, left, right, difficulty, not isPressureFirst)
    Interval(2)

###########################################################

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExpChoice.saveAsWideText(filename+'_Choice'+'.csv', delim='auto')
logging.flush()
# make sure everything is closed down
thisExpRating.abort()  # or data files will save again on exit
thisExpChoice.abort()  # or data files will save again on exit
win.close()
core.quit()
