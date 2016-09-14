####!/usr/bin/arch -i386 /usr/bin/python
# -*- coding: utf-8 -*-
"""
Motion Clouds: SF Bandwidth (B_sf)
2016-07-29
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
# import sys # this was an attempt to make the damn thing work from the terminal
# sys.path.insert(0, "/usr/local/lib/python2.7/site-packages")
from psychopy import visual, core, data, event, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
from datetime import datetime
import os  # handy system and path functions
import itertools
import shutil
import pyglet
import MotionClouds as mc
import pandas as pd
#allScrs = pyglet.window.get_platform().get_default_display().get_screens()

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))

# ====================================================================================
## Initial variables.
###### 7.2dova = 71mm = 256px; 475x296mm, 563mm viewing dist ######
# Window circles (specified in degrees of visual angles [dva]):
windowSize = 7.2 # 5.03; calculated as 5/x=sqrt(2)/2 => x=10/sqrt(2)
windowOffsetX = 6 # 5.62
windowOffsetY = 3.5 # 5.5 (3.5cm ~= 124px)
windowThickness = 4
fdbkLen = .5 # the length of the feedback line
fdbkThick = 5 # the tickness of the feedback line
dimMulti = 35.65 # px/dova (adjusted empirically; calc'd: 35.55)
# Timing variables:
ISIduration = 0.0

dr = (1680,1050)
dd = (47.5,29.6)
def cm2px(cm,dr,dd):
    px = cm*(dr[0]/dd[0])
    return px
def px2cm(px,dr,dd):
    cm = px/(dr[0]/dd[0])
    return cm

# ====================================================================================
# Eye tracking initialization

import pylink as pl
#cp = (0.4,0.4) # calibration proportion
cd = 32

eyeLink = ("100.1.1.1")

displayInfo = pl.getDisplayInformation()
print displayInfo.width, displayInfo.height
screenCenter = (int(dr[0]/2), int(dr[1]/2))
calScreenCenter = (int(screenCenter[0]+cm2px(windowOffsetX,dr,dd)),
                   int(screenCenter[1]-cm2px(windowOffsetY,dr,dd)))
calTargDist = int(cm2px(windowSize,dr,dd)/3)
calTarg1 = calScreenCenter
calTarg2 = (int(calScreenCenter[0]-calTargDist), int(calScreenCenter[1]))
calTarg3 = (int(calScreenCenter[0]+calTargDist), int(calScreenCenter[1]))

def endCalib(el):
    # Ends the recording; adds 100ms to catch final events
    pl.endRealTimeMode()
    pumpDelay(100)
    el.stopRecording()
    while el.getkey():
        pass

def eyeTrkInit (dr):
    el = pl.EyeLink()
    # sending the screen dimensions to the eye tracker:
    el.sendCommand('screen_pixel_coords = 0 0 %d %d' %dr)
    el.sendMessage('DISPLAY_COORDS 0 0 %d %d' %dr)
    el.sendCommand('generate_default_targets = NO')
    el.sendCommand('calibration_targets = %d,%d %d,%d %d,%d' % (
                   calTarg1[0], calTarg1[1],
                   calTarg2[0], calTarg2[1],
                   calTarg3[0], calTarg3[1]) )
    el.sendCommand('validation_targets = %d,%d %d,%d %d,%d' % (
                   calTarg1[0], calTarg1[1],
                   calTarg2[0], calTarg2[1],
                   calTarg3[0], calTarg3[1]) )
    # parser configuration 1 corresponds to high sensitivity to saccades:
    el.sendCommand('select_parser_configuration 1')
    # turns off "scenelink camera stuff", i.e., doesn't record the ET video
    el.sendCommand('scene_camera_gazemap = NO')
    # converting pupil area to diameter
    el.sendCommand('pupil_size_diameter = %s'%('YES'))
    return(el)
el = eyeTrkInit(dr)
print 'Finished initializing the eye tracker.'

def eyeTrkCalib (el,dr,cd):
    # "opens the graphics if the display mode is not set"
    pl.openGraphics(dr,cd)
    pl.setCalibrationColors((255,255,255),(0,177,177))
    pl.setTargetSize(10, 5) 
    pl.setCalibrationSounds("","","")
    el.setCalibrationType('H3')
    pl.setDriftCorrectSounds("","off","off")
    el.disableAutoCalibration()
    el.doTrackerSetup()
    el.drawCalTarget(calTarg1)
    el.drawCalTarget(calTarg2)
    el.drawCalTarget(calTarg3)
    pl.closeGraphics()
    el.setOfflineMode()

def eyeTrkOpenEDF (dfn,el):
    el.openDataFile(dfn + '.EDF')
el.openDataFile('test' + '.EDF')
print '///set up the EDF file for eye-tracking///'

# ====================================================================================
# Setup the Window
win = visual.Window(size=dr, fullscr=False, screen=0, allowGUI=False, 
      allowStencil=False, monitor='testMonitor', color='black', colorSpace='rgb', 
      blendMode='avg', useFBO=True, units='deg')
# store frame rate of monitor if we can measure it successfully:
frameRate=win.getActualFrameRate()
if frameRate!=None:
    frameDur = 1.0/round(frameRate)
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# ====================================================================================
from psychopy.iohub import launchHubServer
io = launchHubServer()
kb_device = io.devices.keyboard

# ====================================================================================
# Eye-tracking setup

kb_device.clearEvents()
def etSetup(el,dr,cd):
    blockLabel=visual.TextStim(win, text="Press the space bar to begin drift                                                                         correction", pos=[0,0], color="white", bold=True,
                               alignHoriz="center", height=0.5)
    notdone=True
    while notdone:
        blockLabel.draw()
        win.flip()
        keySpace = kb_device.getPresses(keys=[' ','escape'])
        if ' ' in keySpace:
            print 'spacebar pressed'
            eyeTrkCalib(el,dr,cd)
            win.winHandle.activate()
            print '///Finished calibration///'
            notdone=False
        elif 'escape' in keySpace:
            print 'procedure terminated'
            notdone=False
etSetup(el,dr,cd)

def drCor(el,dr,cd):
    pl.openGraphics(dr,cd)
    el.doDriftCorrect(calScreenCenter[0], calScreenCenter[1], 1, 0)
    pl.closeGraphics()
    print '///Finished drift correction///'

# ====================================================================================

# Store info about the experiment session
expName = 'mcbsf'  # from the Builder filename that created this script
expInfo = {u'session': u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName) # dialogue box
if dlg.OK == False: core.quit()  # user pressed cancel
timeNow = datetime.now()
expInfo['time'] = datetime.now().strftime('%Y-%m-%d_%H%M')
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
precompileMode = 0
if precompileMode:
    precompiledDir = '..' + os.sep + 'precompiledMCs'
grtSize = 256 # size of 256 is 71mm, or 7.2dova
dataDir = '..' + os.sep + 'data'
fileName = '%s_p%s_s%s_%s' %(expName, expInfo['participant'], expInfo['session'],
    expInfo['time'])
filePath = dataDir + os.sep + fileName
print filePath

# Condition-related variables
conditionsFilePath = 'cond-files'+os.sep+'cond-'+expName+'-test.csv' #TEMP
print conditionsFilePath
os.chdir(_thisDir)

# ====================================================================================

endExpNow = False  # flag for 'escape' or other condition => quit the exp

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
    end=[-windowOffsetX+(windowSize/2)+fdbkLen, windowOffsetY], lineColor='white',
    lineWidth=fdbkThick)
feedbackRight = visual.Line(win=win, start=[windowOffsetX+windowSize/2, windowOffsetY],
    end=[windowOffsetX+(windowSize/2)+fdbkLen, windowOffsetY], lineColor='white',
    lineWidth=fdbkThick)
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

# An empty data set for storing behavioural responses:
behResp = []
    
# Printing the attributes of the conds:  
print commonNTrials
trials = data.TrialHandler(conds, commonNTrials, extraInfo=expInfo)
# Creating a copy of the Conditions file for book-keeping and analyses:
if not os.path.exists(filePath):
    os.makedirs(filePath)
shutil.copyfile(conditionsFilePath, filePath + os.sep + 
                os.path.basename(conditionsFilePath))
dataFileName = filePath + os.sep + fileName + '.csv'

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

win.winHandle.minimize()
win.flip()
drCor(el,dr,cd)
win.winHandle.maximize()
win.flip()
win.winHandle.activate()

# ====================================================================================
# Initiating the trial loop

nDone=0
for thisTrial in trials:
    print '===new=trial==='
    nDone += 1
    print 'trial#' + str(nDone)
    dirL = thisTrial['dirL']
    dirR = thisTrial['dirR']
    print 'dirL=' + str(dirL) + '; dirR=' + str(dirR)
    vL = thisTrial['vL']
    vR = thisTrial['vR']
    print 'vL=' + str(vL) + '; vR=' + str(vR)
    szL = thisTrial['szL']
    szR = thisTrial['szR']
    print 'szL=' + str(szL) + '; szR=' + str(szR)
    sfL = thisTrial['sfL']
    sfR = thisTrial['sfR']
    print 'sfL=' + str(sfL) + '; sfR=' + str(sfR)
    tfL = thisTrial['tfL']
    tfR = thisTrial['tfR']
    if tfL != 'NA':
    #if np.isnan(tfL):
        tfL = vL * sfL # doesn't matter if sfX or sfY
    if tfR != 'NA':
    #if np.isnan(tfR):
        tfR = vR * sfR
    # print 'tfL=' + thisTfL + '; tfR=' + thisTfR
    BsfL = thisTrial['BsfL']
    BsfR = thisTrial['BsfR']
    print 'BsfL=' + str(BsfL) + '; BsfR=' + str(BsfR)
    trialT = thisTrial['trialT'] # -win.monitorFramePeriod*0.75
    nFrames = 60 # number of frames per sequence
    
    # Creating an empty matrix for keeping the behavioural responses:
    behRespTrial = np.empty([1, trialT*nFrames]) 
    behRespTrial[:] = np.NAN
    
    # initiating the gratings
    if precompileMode:
        grtL = np.load(precompiledDir + os.sep + expName + '_' + str(vL) +
               '_sf' + str(sfL) + '_bsf' + str(BsfL) + '_sz' + str(szL) + '.npy')
        grtR = np.load(precompiledDir + os.sep + expName + '_' + str(vR) +
               '_sf' + str(sfR) + '_bsf' + str(BsfR) + '_sz' + str(szR) + '.npy')
    else:
        fx, fy, ft = mc.get_grids(szL, szL, nFrames)
        grtCol = mc.envelope_color(fx, fy, ft)
        grtL = 2*mc.rectif(mc.random_cloud(grtCol * 
               mc.envelope_gabor(fx, fy, ft, sf_0=sfL, B_sf=BsfL,
               V_X=vL, B_theta=np.inf))) - 1
        fx, fy, ft = mc.get_grids(szR, szR, nFrames)
        grtCol = mc.envelope_color(fx, fy, ft)
        grtR = 2*mc.rectif(mc.random_cloud(grtCol * 
               mc.envelope_gabor(fx, fy, ft, sf_0=sfR, B_sf=BsfR,
               V_X=vR, B_theta=np.inf))) - 1

    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    tMaskMove = 0
    key_pressed = False
    key_pause = False
    key_qn = False
    behRespRecorded = False
    someKeyPressed = False # to prevent recording key releases at trial beginning
    windowLeft.lineColor = 'white'
    windowRight.lineColor = 'white'
    # update component parameters for each repeat
    key_arrow = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_arrow.status = NOT_STARTED
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
    trialComponents.append(pauseTextLeft)
    trialComponents.append(pauseTextRight)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # ////////////////////////////////////////////////////////////////////////////////
    #win.winHandle.minimize()
    #drCor(el,dr,cd)
    #win.winHandle.maximize()
    #win.winHandle.activate()
    el.sendMessage("TRIALID " + str(nDone))
    trialStartStr = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    el.sendMessage("TIMESTAMP " + trialStartStr)
    el.setOfflineMode()
    #msecDelay(50) 
    #error = el.startRecording(1,1,1,1)
    # ////////////////////////////////////////////////////////////////////////////////
    
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
            windowLeft.status = STARTED
        
        # *windowRight* updates
        if windowRight.status == NOT_STARTED:
            # keep track of start time/frame for later
            windowRight.tStart = t  # underestimates by a little under one frame
            windowRight.frameNStart = frameN  # exact frame index
            windowRight.setAutoDraw(True)
            windowRight.status = STARTED

        # stimulus presentation:
        if t < trialT:
            stimL = visual.GratingStim(win, tex=grtL[:,:,frameN%nFrames], 
                size=(grtSize,grtSize), units='pix', 
                pos=(-windowOffsetX*dimMulti, windowOffsetY*dimMulti),
                interpolate=False, mask='circle', ori=90+dirL)
            stimL.draw()
            stimR = visual.GratingStim(win, tex=grtR[:,:,frameN%nFrames], 
                size=(grtSize,grtSize), units='pix', 
                pos=(windowOffsetX*dimMulti, windowOffsetY*dimMulti),
                interpolate=False, mask='circle', ori=90+dirR)
            stimR.draw()
        
        # *key_arrow* updates
        if key_arrow.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_arrow.tStart = t  # underestimates by a little under one frame
            key_arrow.frameNStart = frameN  # exact frame index
            key_arrow.status = STARTED
            # keyboard checking is just starting
            key_arrow.clock.reset()  # now t=0
            event.clearEvents(eventType='keyboard')
            kb_device.clearEvents()
        if key_arrow.status == STARTED and t < trialT:
            # theseKeys = event.getKeys(keyList=['left','right','down'])
            # print kb_device.getKeys()
            thesePresses = kb_device.getPresses(keys=['left','right','down','escape'])
            # print thesePresses
            theseReleases = kb_device.getReleases(keys=['left','right','down'])
            # print theseReleases
            # check for quit:
            if len(thesePresses) > 0:
                feedbackLeft.setAutoDraw(True)
                feedbackRight.setAutoDraw(True)
                keyPressFN = frameN
                someKeyPressed = True
                if 'left' in thesePresses:
                    print '"left" key is pressed'
                    feedbackLeft.start = [-windowOffsetX-windowSize/2, windowOffsetY]
                    feedbackLeft.end = [-windowOffsetX-(windowSize/2)-fdbkLen,
                        windowOffsetY]
                    feedbackRight.start = [windowOffsetX-windowSize/2, windowOffsetY]
                    feedbackRight.end = [windowOffsetX-(windowSize/2)-fdbkLen,
                        windowOffsetY]
                    whichKeyPressed = 'left' # only needed for final key press
                elif 'right' in thesePresses:
                    print '"right" key is pressed'
                    feedbackLeft.start = [-windowOffsetX+windowSize/2, windowOffsetY]
                    feedbackLeft.end = [-windowOffsetX+(windowSize/2)+fdbkLen,
                                         windowOffsetY]
                    feedbackRight.start = [windowOffsetX+windowSize/2, windowOffsetY]
                    feedbackRight.end = [windowOffsetX+(windowSize/2)+fdbkLen,
                                         windowOffsetY]
                    whichKeyPressed = 'right'
                elif 'down' in thesePresses:
                    print '"down" key is pressed'
                    feedbackLeft.start = [-windowOffsetX, windowOffsetY-windowSize/2]
                    feedbackLeft.end = [-windowOffsetX,
                                        windowOffsetY-(windowSize/2)-fdbkLen]
                    feedbackRight.start = [windowOffsetX, windowOffsetY-windowSize/2]
                    feedbackRight.end = [windowOffsetX,
                                         windowOffsetY-(windowSize/2)-fdbkLen]
                    whichKeyPressed = 'down'
                else:
                    print 'some other key is pressed'
            if len(theseReleases) > 0 and someKeyPressed:
                feedbackLeft.setAutoDraw(False)
                feedbackRight.setAutoDraw(False)
                print '...released after ' + \
                      str(np.around((frameN-keyPressFN)/60,2)) + 's'
                someKeyPressed = False
                if 'left' in theseReleases:
                    behRespTrial[0,keyPressFN:frameN+1] = 180 # left
                elif 'right' in theseReleases:
                    behRespTrial[0,keyPressFN:frameN+1] = 0 # right
                elif 'down' in theseReleases:
                    behRespTrial[0,keyPressFN:frameN+1] = 270 # down
                else:
                    print 'some other key is released'
                # print 'no key is currently released'

        # after-trial question about the trial stability
        if ~key_qn and t > trialT:
            qntxtLeft.setAutoDraw(True)
            qntxtRight.setAutoDraw(True)
            thesePresses = kb_device.getPresses(keys=['1','2','3','4'])
            if len(thesePresses)>0:
                if '1' in thesePresses:
                    qnResp = 1
                elif '2' in thesePresses:
                    qnResp = 2
                elif '3' in thesePresses:
                    qnResp = 3
                elif '4' in thesePresses:
                    qnResp = 4
                key_qn = True

        # pause text and data exporting
        if key_qn and ~key_pause and t > trialT:
            qntxtLeft.setAutoDraw(False)
            qntxtRight.setAutoDraw(False)
            pauseTextLeft.setAutoDraw(True)
            pauseTextRight.setAutoDraw(True)
            if not behRespRecorded: # a flag for data recording
                # Make sure to record the release of a key at trial end
                if someKeyPressed:
                    if whichKeyPressed == 'left':
                        behRespTrial[0,keyPressFN:(trialT*nFrames)] = 180
                    if whichKeyPressed == 'right':
                        behRespTrial[0,keyPressFN:(trialT*nFrames)] = 0
                    if whichKeyPressed == 'down':
                        behRespTrial[0,keyPressFN:(trialT*nFrames)] = 270
                    feedbackLeft.setAutoDraw(False)
                    feedbackRight.setAutoDraw(False)
                    print '...released after ' + \
                        str(np.around(((trialT*nFrames)-keyPressFN)/60,2)) + 's'
                    print 'recorded post-trial response'
                # Recording the responses:
                if len(behResp)>0:
                    behResp = np.vstack((behResp, behRespTrial))
                else: 
                    behResp = behRespTrial
                behRespRecorded = True
                # Computing and recording predominance:
                nNa = np.count_nonzero(np.isnan(behRespTrial))
                nf000 = np.count_nonzero(behRespTrial==0)
                nf180 = np.count_nonzero(behRespTrial==180)
                nf270 = np.count_nonzero(behRespTrial==270)
                dT = pd.DataFrame({'expName': expName,
                                   'time': expInfo['time'],
                                   'participant': expInfo['participant'],
                                   'session': expInfo['session'],
                                   'trialN': nDone,
                                   'dirL': dirL, 'dirR': dirR,
                                   'vL': vL, 'vR': vR, 'szL': szL, 'szR': szR,
                                   'sfL': sfL, 'sfR': sfR, 'tfL': tfL, 'tfR': tfR,
                                   'BsfL': BsfL, 'BsfR': BsfR,
                                   'trialT': trialT, 'nFrames': nFrames, 'nNa': nNa,
                                   'nf000': nf000, 'nf180': nf180, 'nf270': nf270,
                                   'pd000': [nf000 / (trialT * nFrames)],
                                   'pd180': [nf180 / (trialT * nFrames)],
                                   'pd270': [nf270 / (trialT * nFrames)],
                                   'qnResp': qnResp})
                # to preserve the column order:
                dataCols = ['expName', 'time', 'participant', 'session', 'trialN',
                            'dirL', 'dirR', 'vL', 'vR', 'szL', 'szR', 'sfL', 'sfR',
                            'tfL', 'tfR', 'BsfL', 'BsfR', 'trialT', 'nFrames', 'nNa',
                            'nf000', 'nf180', 'nf270', 'pd000', 'pd180', 'pd270', 'qnResp']
                if nDone == 1:
                    df = dT
                else:
                    df = pd.concat([df,dT])
                # Recording the data to a csv file:
                df.to_csv(dataFileName, index=False, columns=dataCols)
                print 'wrote the data set to ' + dataFileName
            if 'space' in event.getKeys(keyList=['space']):
                print 'spacebar pressed - continuing to the next trial'
                key_pause = True

        # wait for the presentation time to pass to terminate the trial:
        if t>=trialT and key_pause:
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
            print np.shape(behResp)
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

    # thisExp.nextEntry()

# trialsFilePath = filePath + os.sep + fileName + '_trials'
# trials.saveAsPickle(trialsFilePath)
# trials.saveAsText(trialsFilePath)
# print trials
print "finished the experiment"

win.close()
core.quit()
