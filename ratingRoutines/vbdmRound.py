from .components import *
from psychopy import core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard

frameTolerance = 0.001  # how close to onset before 'same' frame
endExpNow = False  # flag for 'escape' or other condition => quit the exp

leftImg = visual.ImageStim(
    win=win,
    name='leftImage', 
    image=None, mask=None,
    ori=0.0, pos=(-180, 100), size=(180),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

rightImg = visual.ImageStim(
    win=win,
    name='rightImage', 
    image=None, mask=None,
    ori=0.0, pos=(180, 100), size=(180),
    color=[1,1,1], colorSpace='rgb', opacity=None,
    flipHoriz=False, flipVert=False,
    texRes=128.0, interpolate=True, depth=0.0)

key_Choice = keyboard.Keyboard()


def VBDM(thisExp, leftPic, rightPic, difficulty, isTimePressure):
    # setup image
    leftImg.image = 'Face Choose/'+leftPic
    rightImg.image = 'Face Choose/' + rightPic

    # ------Prepare to start Routine "trial"-------
    continueRoutine = True
    if isTimePressure:
        routineTimer.add(2) #  choicetime
    # update component parameters for each repeat
    # setup some python lists for storing info about the mouse
    key_Choice.keys = []
    key_Choice.rt = []
    _key_Choice_allKeys = []
    # keep track of which components have finished
    trialComponents = [leftImg, rightImg, key_Choice]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1

    # -------Run Routine "trial"-------
    # time1 = trialClock.getTime()
    while continueRoutine:
        if isTimePressure and routineTimer.getTime() <= 0:
            continueRoutine = False

        # get current time
        t = trialClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=trialClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *leftImg* updates
        if leftImg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            leftImg.frameNStart = frameN  # exact frame index
            leftImg.tStart = t  # local t and not account for scr refresh
            leftImg.tStartRefresh = tThisFlipGlobal  # on global time
            # time1g = tThisFlipGlobal
            win.timeOnFlip(leftImg, 'tStartRefresh')  # time at next scr refresh
            leftImg.setAutoDraw(True)

        # *rightImg* updates
        if rightImg.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            rightImg.frameNStart = frameN  # exact frame index
            rightImg.tStart = t  # local t and not account for scr refresh
            rightImg.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(rightImg, 'tStartRefresh')  # time at next scr refresh
            rightImg.setAutoDraw(True)

        # *key_Choice* updates
        waitOnFlip = False
        if key_Choice.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_Choice.frameNStart = frameN  # exact frame index
            key_Choice.tStart = t  # local t and not account for scr refresh
            key_Choice.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_Choice, 'tStartRefresh')  # time at next scr refresh
            key_Choice.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_Choice.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_Choice.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_Choice.status == STARTED and not waitOnFlip:
            theseKeys = key_Choice.getKeys(keyList=['right', 'left'], waitRelease=True)
            _key_Choice_allKeys.extend(theseKeys)
            if len(_key_Choice_allKeys):
                continueRoutine = False
                # time2 = trialClock.getTime()
                # time2g = tThisFlipGlobal
                key_Choice.keys = _key_Choice_allKeys[-1].name  # just the last key pressed
                key_Choice.rt = _key_Choice_allKeys[-1].rt

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        thisComponent.tStopRefresh = tThisFlipGlobal
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    thisExp.addData('Trial', str(difficulty)+'_'+leftPic[:-4]+"_"+rightPic[:-4])
    thisExp.addData('choice', key_Choice.keys)
    thisExp.addData('RT', key_Choice.rt)
    thisExp.addData('key.started', key_Choice.tStartRefresh)
    thisExp.addData('key.stopped', key_Choice.tStopRefresh)
    # store data for thisExp (ExperimentHandler)

    thisExp.nextEntry()
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

