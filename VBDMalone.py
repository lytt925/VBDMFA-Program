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
from itertools import count

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.0'
expName = 'VBDM'  # from the Builder filename that created this script
expInfo = {'participant': '', 'RatingPath':''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr(
    format="%Y-%m-%d-%H%M")  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

from ratingRoutines.components import *
from ratingRoutines.makeStim import makeStim
from ratingRoutines.vbdmRound import *
from ratingRoutines.ratings import singleImage

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + \
    u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExpChoice = data.ExperimentHandler(name=expName+'_Choice', version='',
                                       extraInfo=expInfo, runtimeInfo=None,
                                       savePickle=False, saveWideText=True,
                                       dataFileName=filename+'_Choice')

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

# Setup eyetracking
ioDevice = ioConfig = ioSession = ioServer = eyetracker = None


# Start Code - component code to be run after the window creation

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

###########################################################

StartInterface()
RatingPath = expInfo['RatingPath']

###########################################################
Rating = pd.read_csv('data/'+RatingPath)
Rating = Rating.sort_values(
    'Name', key=lambda x: sorted(x.str.slice(start=2, stop=-4)))
Rating.loc[Rating.query('rating==10').index, 'rating'] = 9
ratings_counts = Rating['rating'].value_counts()
print('ratings_counts', ratings_counts)
allcounts = [ratings_counts[i] for i in range(5, 10)]
temp = [list(np.repeat(i+5, count)) for i, count in enumerate(allcounts)]
ratings = [[str(level)+'_'+str(ind+1)
            for ind, level in enumerate(levelList)] for levelList in temp]
stimDict = {}
for i, level in enumerate(ratings):
    iterator = iter(list(Rating[Rating['rating'] == i+5]['Name']))
    for key in level:
        stimDict[key] = next(iterator)

text_end.text = 'Loading'
text_end.draw()
win.flip()
stimList1, stimList2 = makeStim(allcounts)
win.flip()
stimList1_All = [stim for diffList in stimList1 for stim in diffList]
np.random.shuffle(stimList1_All)
stimList2_All = [stim for diffList in stimList2 for stim in diffList]
np.random.shuffle(stimList2_All)

correctCounter = 0
##########################################################
isPressureFirst = bool(int(expInfo['participant']) % 2)
if isPressureFirst:
    instructionImg = './ratingRoutines/Pressure.png'
else:
    instructionImg = './ratingRoutines/noPressure.png'

InstructionInterface(instructionImg)
firstRound = count()
for stim in stimList1_All:
    c = next(firstRound)
    if c % 50 == 0 and c != 0:
        restInterface()   
    Interval(2)
    difficulty = abs(int(stim[1].split('_')[0])-int(stim[0].split('_')[0]))
    leftInd = np.random.randint(2)
    rightInd = abs(leftInd-1)
    left = stimDict[stim[leftInd]]
    right = stimDict[stim[rightInd]]
    # print(left, stim[leftInd])
    # print(right, stim[rightInd])
    if int(stim[leftInd][0]) > int(stim[rightInd][0]):
        # print('left big')
        corAns = 'left'
    elif int(stim[leftInd][0]) < int(stim[rightInd][0]):
        corAns = 'right'
        # print('right big')
    # print('corAns',corAns)
    VBDM(thisExpChoice, left, right, difficulty, isPressureFirst, corAns=corAns)

########################################################
if not isPressureFirst:
    instructionImg = './ratingRoutines/Pressure.png'
else:
    instructionImg = './ratingRoutines/noPressure.png'

InstructionInterface(instructionImg)

secRound = count()
for stim in stimList2_All:
    c = next(secRound)
    if c % 50 == 0 and c != 0:
        restInterface()   
    Interval(2)
    difficulty = abs(int(stim[1].split('_')[0])-int(stim[0].split('_')[0]))
    leftInd = np.random.randint(2)
    rightInd = abs(leftInd-1)
    left = stimDict[stim[leftInd]]
    right = stimDict[stim[rightInd]]
    if int(stim[leftInd][0]) > int(stim[rightInd][0]):
        corAns = 'left'
    elif int(stim[leftInd][0]) < int(stim[rightInd][0]):
        corAns = 'right'
    VBDM(thisExpChoice, left, right, difficulty, not isPressureFirst, corAns=corAns)

##########################################################
thisExpChoice.saveAsWideText(filename+'_ChoiceBackup'+'.csv', delim=',')
VBDMresult = pd.read_csv(filename+'_ChoiceBackup'+'.csv')
accuracy = VBDMresult['Correct'].replace({'None': 0}).astype(int).mean()
EndInterface(accuracy)

############################################################
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
# thisExpChoice.saveAsWideText(filename+'_Choice'+'.csv', delim=',')
logging.flush()
# make sure everything is closed down
thisExpChoice.abort()  # or data files will save again on exit
win.close()
core.quit()
