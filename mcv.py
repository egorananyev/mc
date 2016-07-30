#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Motion Clouds: Velocity
2016-07-29
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, gui #,logging
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
from datetime import datetime
import os  # handy system and path functions
import itertools
import shutil
import pyglet
allScrs = pyglet.window.get_platform().get_default_display().get_screens()
print allScrs
# Import the threshold information for the subject:

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'mcv'  # from the Builder filename that created this script
expInfo = {u'session': u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName) # dialogue box
if dlg.OK == False: core.quit()  # user pressed cancel
timeNow = datetime.now()
expInfo['date'] = datetime.now().strftime('%Y-%m-%d_%H%M')
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
dataDir = '..' + os.sep + 'data'
fileName = '%s_p%s_s%s_%s' %(expName, expInfo['participant'], expInfo['session'],
    expInfo['date'])
filePath = dataDir + os.sep + fileName
print filePath

# ====================================================================================
## Initial variables.
# Window circles (specified in degrees of visual angles [dva]):
windowSize = 7.07 # 5.03; calculated as 5/x=sqrt(2)/2 => x=10/sqrt(2)
windowOffsetX = 5.62 # 5.62 # 6.71
windowOffsetY = 5.5 # 2.83 # 4.97
windowThickness = 2
# Timing variables:
ISIduration = 0.0
# Condition-related variables
conditionsFilePath = 'cond-files'+os.sep+'cond-mcv'+'.csv'
print conditionsFilePath
# ====================================================================================

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='', extraInfo=expInfo, 
    runtimeInfo=None, originPath=None, savePickle=True, saveWideText=True, 
    dataFileName=filePath)

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1680, 1050), fullscr=False, screen=1, allowGUI=False, 
    allowStencil=False, monitor='testMonitor', color='black', colorSpace='rgb', 
    blendMode='avg', useFBO=True, units='deg')
# store frame rate of monitor if we can measure it successfully
frameRate=win.getActualFrameRate()
if frameRate!=None:
    frameDur = 1.0/round(frameRate)
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instrText = visual.TextStim(win=win, ori=0, name='instrText',
    text='Press any key to start', font='Cambria', pos=[0, 0], height=1, wrapWidth=10,
    color='white', colorSpace='rgb', opacity=1)

# Initialize components for Routine "trial"
trialClock = core.Clock()
moveClock = core.Clock()
maskMoveClock = core.Clock()
windowLeft = visual.Polygon(win=win, name='windowLeft', units='deg', edges=36,
    size=[windowSize, windowSize], ori=0, pos=[-windowOffsetX, windowOffsetY],
    lineWidth=windowThickness, lineColor=u'white', lineColorSpace='rgb',
    fillColor=None, opacity=1, interpolate=True)
windowRight = visual.Polygon(win=win, name='windowRight', units='deg', edges=36,
    size=[windowSize, windowSize], ori=0, pos=[windowOffsetX, windowOffsetY],
    lineWidth=windowThickness, lineColor=u'white', lineColorSpace='rgb',
    fillColor=None, opacity=1, interpolate=True)
feedbackLeft = visual.Line(win=win, start=[-windowOffsetX+windowSize/2, windowOffsetY],
    end=[-windowOffsetX+(windowSize/2)+.1, windowOffsetY], lineColor='white')
feedbackRight = visual.Line(win=win, start=[windowOffsetX+windowSize/2, windowOffsetY],
    end=[windowOffsetX+(windowSize/2)+.1, windowOffsetY], lineColor='white')
ISI = core.StaticPeriod(win=win, screenHz=frameRate, name='ISI')
# setting the edges to 3 (triangle) initially: this will change once ...
# ... the attributes are read from the configuration file:
target = visual.Polygon(win=win, name='target',units='deg', edges = 3, size=[0.1, 0.1],
    ori=45, pos=[0, 0], lineWidth=1, lineColor=1.0, lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb', opacity=1, interpolate=True)
# question text:
qntxtLeft = visual.TextStim(win=win, name='qntxtLeft',
    text='1=not stable\n2=not very stable\n3=almost stable\n4=completely stable',
    font='Cambria', pos=[-windowOffsetX, windowOffsetY], height=.55, wrapWidth=4.5,
    color='white', colorSpace='rgb', opacity=1)
qntxtRight = visual.TextStim(win=win, name='qntxtRight',
    text='1=not stable\n2=not very stable\n3=almost stable\n4=completely stable',
    font='Cambria', pos=[windowOffsetX, windowOffsetY], height=.55, wrapWidth=4.5,
    color='white', colorSpace='rgb', opacity=1)
# pause text:
pauseTextLeft = visual.TextStim(win=win, ori=0, name='pauseTextLeft',
    text='Press Spacebar to continue.', font='Cambria', alignHoriz='center',
    pos=[-windowOffsetX, windowOffsetY], height=.7, wrapWidth=3, color='white',
    colorSpace='rgb', opacity=1)
pauseTextRight = visual.TextStim(win=win, ori=0, name='pauseTextRight',
    text='Press Spacebar to continue.', font='Cambria', alignHoriz='center',
    pos=[windowOffsetX, windowOffsetY], height=.7, wrapWidth=3, color='white',
    colorSpace='rgb', opacity=1)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
instrKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
instrKey.status = NOT_STARTED
# keep track of which components have finished
instructionsComponents = []
instructionsComponents.append(instrText)
instructionsComponents.append(instrKey)
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED


# ====================================================================================
# Setting up the conditions:
condList = data.importConditions(conditionsFilePath)
conds = []
commonNTrials = []
for thisCondition in condList:
    nTrials = thisCondition['trialN']
    # print 'Number of trials in this condition: ' + str(nTrials)
    conds.append(thisCondition)
    commonNTrials = nTrials
    
# Printing the attributes of the conds:  
print commonNTrials
trials = data.TrialHandler(conds, commonNTrials, extraInfo=expInfo)
trials.data.addDataType('pd0') # predominance of rightward motion
trials.data.addDataType('pd180') # predominance of leftward motion
trials.data.addDataType('pdNone') # no predominance (transparancy / unclear) at 90 or 270
# Creating a copy of the Conditions file for book-keeping and analyses:
if not os.path.exists(filePath):
    os.makedirs(filePath)
shutil.copyfile(conditionsFilePath, filePath + os.sep + os.path.basename(conditionsFilePath))

#-------Start Routine "instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrText* updates
    if t >= 0.0 and instrText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText.tStart = t  # underestimates by a little under one frame
        instrText.frameNStart = frameN  # exact frame index
        instrText.setAutoDraw(True)
    
    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
        windowLeft.setAutoDraw(True)
        windowRight.setAutoDraw(True)
    if instrKey.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()
    else:  # this Routine was not non-slip safe so reset non-slip timer
        routineTimer.reset()

#-------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# ====================================================================================
# Initiating the trial loop

nDone=0
for thisTrial in trials:
    print '===new=trial==='
    nDone += 1
    print 'trial#' + str(nDone)
    # trials.data.add('thisTargDir', thisTargDir)
    thisDirL = thisTrial['dirL']
    thisDirR = thisTrial['dirR']
    trials.data.add('thisDirL', thisDirL)
    trials.data.add('thisDirR', thisDirR)
    thisVL = thisTrial['vL']
    thisVR = thisTrial['vR']
    trials.data.add('thisVL', thisVL)
    trials.data.add('thisVR', thisVR)
    print thisTrial['label']
    thisSfLx = thisTrial['sfLx']
    thisSfRx = thisTrial['sfRx']
    trials.data.add('thisSfLx', thisSfLx)
    trials.data.add('thisSfRx', thisSfRx)
    # print 'sfLx=' + thisSfLx + '; sfRx=' + thisSfRx
    thisSfLy = thisTrial['sfLy']
    thisSfRy = thisTrial['sfRy']
    trials.data.add('thisSfLy', thisSfLy)
    trials.data.add('thisSfRy', thisSfRy)
    # print 'sfLy=' + thisSfLy + '; sfRy=' + thisSfRy
    thisTfL = thisTrial['tfL']
    thisTfR = thisTrial['tfR']
    if np.isnan(thisTfL):
        thisTfL = thisVL * thisSfLx # doesn't matter if sfX or sfY
    if np.isnan(thisTfR):
        thisTfR = thisVR * thisSfRx
    trials.data.add('thisTfL', thisTfL)
    trials.data.add('thisTfR', thisTfR)
    # print 'tfL=' + thisTfL + '; tfR=' + thisTfR
    thisBsfL = thisTrial['BsfL']
    thisBsfR = thisTrial['BsfR']
    trials.data.add('thisBsfL', thisBsfL)
    trials.data.add('thisBsfR', thisBsfR)
    # print 'BsfL=' + thisBsfL + '; BsfR=' + thisBsfR
    thisTrialT = thisTrial['trialT']-win.monitorFramePeriod*0.75
    
    # initiating the grating
    fx, fy, ft = mc.get_grids(szX, szY, N_frame_total)
    colorGr = mc.envelope_color(fx, fy, ft)
    leftGr = 2*mc.rectif(mc.random_cloud(colorGr * mc.envelope_gabor(fx, fy, ft, V_X=+.5))) - 1
    leftGr = 2*mc.rectif(mc.random_cloud(colorGr * mc.envelope_gabor(fx, fy, ft, V_X=-.5))) - 1
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    tMaskMove = 0
    key_pressed = False
    key_pause = False
    windowLeft.lineColor = 'white'
    windowRight.lineColor = 'white'
    # update component parameters for each repeat
    key_arrow = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_arrow.status = NOT_STARTED
    key_space = event.BuilderKeyResponse()
    key_space.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(windowLeft)
    trialComponents.append(windowRight)
    trialComponents.append(ISI)
    trialComponents.append(feedbackLeft)
    trialComponents.append(feedbackRight)
    trialComponents.append(qntxtLeft)
    trialComponents.append(qntxtRight)
    trialComponents.append(key_arrow)
    trialComponents.append(key_space)
    trialComponents.append(pauseTextLeft)
    trialComponents.append(pauseTextRight)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1 # number of completed frames (0 is the first frame)
        # update/draw components on each frame
        
        # *windowLeft* updates
        if windowLeft.status == NOT_STARTED:
            # keep track of start time/frame for later
            windowLeft.tStart = t  # underestimates by a little under one frame
            windowLeft.frameNStart = frameN  # exact frame index
            windowLeft.setAutoDraw(True)
        
        # *windowRight* updates
        if windowRight.status == NOT_STARTED:
            # keep track of start time/frame for later
            windowRight.tStart = t  # underestimates by a little under one frame
            windowRight.frameNStart = frameN  # exact frame index
            windowRight.setAutoDraw(True)

        # pause text (after the response is made):
        if ~key_pause and t > thisTrialT:
            qntxtLeft.setAutoDraw(False)
            qntxtRight.setAutoDraw(False)
            pauseTextLeft.setAutoDraw(True)
            pauseTextRight.setAutoDraw(True)
            if 'space' in event.getKeys(keyList=['space']):
                print 'spacebar pressed - continuing to the next trial'
                key_pause = True

        # *target* updates
        if target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart = t  # underestimates by a little under one frame
            target.frameNStart = frameN  # exact frame index
            target.setAutoDraw(True)
            feedbackLeft.setAutoDraw(True)
            feedbackRight.setAutoDraw(True)
            moveClock.reset()
        if target.status == STARTED and t<thisTrialT:
            curFrameN = frameN - target.frameNStart
        if target.status == STARTED and t >= thisTrialT:
            target.setAutoDraw(False)
            feedbackLeft.setAutoDraw(False)
            feedbackRight.setAutoDraw(False)
        
        # *key_arrow* updates
        if key_arrow.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_arrow.tStart = t  # underestimates by a little under one frame
            key_arrow.frameNStart = frameN  # exact frame index
            key_arrow.status = STARTED
            # keyboard checking is just starting
            key_arrow.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
        if key_arrow.status == STARTED:
            theseKeys = event.getKeys(keyList=['space'])
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0 and not key_pressed:
                print 'key pressed'
                thisRT = key_arrow.clock.getTime()
                key_pressed = True

        # wait for the presentation time to pass to terminate the trial:
        if t>=thisTrialT and key_pause:
            if not key_pressed:
                print 'no response was made'
                trials.data.add('RT', 0)
            else:
                print 'RT: ' + str(thisRT)
                trials.data.add('RT', thisRT)
            continueRoutine = False

        # *ISI* period
        if ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(ISIduration)
        #one frame should pass before updating params and completing
        elif ISI.status == STARTED: 
            ISI.complete() #finish the static period
        
        # check if all components have finished
        # a component has requested a forced-end of Routine:
        if not continueRoutine: 
            # if we abort early the non-slip timer needs reset:
            routineTimer.reset() 
            break
        # will revert to True if at least one component still running
        continueRoutine = False  
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and \
                    thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        # don't flip if this routine is over or we'll get a blank screen
        if continueRoutine:  
            win.flip()
        else: # this Routine was not non-slip safe so reset non-slip timer
            routineTimer.reset()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    thisExp.nextEntry()

trialsFilePath = filePath + os.sep + fileName + '_trials'
trials.saveAsPickle(trialsFilePath)
trials.saveAsText(trialsFilePath)
print trials
print "finished the experiment"

win.close()
core.quit()
