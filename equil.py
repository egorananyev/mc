####!/usr/bin/arch -i386 /usr/bin/python
# -*- coding: utf-8 -*-
"""
Motion Clouds: SF Bandwidth (B_sf)
2016-07-29
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np
import pandas as pd
from datetime import datetime
import os, shutil, itertools  # handy system and path functions
#import pyglet
import MotionClouds as mc

#Initiating the keyboard
from psychopy.iohub import launchHubServer
io = launchHubServer()
kb_device = io.devices.keyboard

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))

# ====================================================================================
## Initial variables.
et = 0
expName = 'equil' # v=velocity, bsf = SF bandwidth, fp = foveal/peripheral, ct = central task
# Window circles (specified in degrees of visual angles [dva]):
#winSz = 7.2 # 5.03; calculated as 5/x=sqrt(2)/2 => x=10/sqrt(2)
winOffX = 6 # 5.62
winOffY = 3.5 # 5.5 (3.5cm ~= 124px)
winThickness = 2 # in pixels
fdbkLen = .5 # the length of the feedback line, in degrees
fdbkThick = 5 # the tickness of the feedback line, in pixels
# Timing variables:
ISIduration = 1
fixSz = .15
# MCs:
precompileMode = 1 # get the precompiled MCs
grtSize = 256 # size of 256 is 71mm, or 7.2dova
defAlpha = .2 # default alpha
# Dimensions:
###### 7.2dova = 71mm = 256px; 475x296mm, 563mm viewing dist ######
dr = (1680,1050) # display resolution in px
dd = (29.5,16.6)
ds = 49.5 # distance to screen in cm
nFrames = 60

# ====================================================================================
# Converter functions:
def cm2px(cm,dr=dr,dd=dd):
    px = int(cm*(dr[0]/dd[0]))
    return px
def px2cm(px,dr=dr,dd=dd):
    cm = px/(dr[0]/dd[0])
    return cm
def cm2dg(cm,ds=ds):
    dg = np.degrees(np.arctan(cm/ds))
    return dg
def dg2cm(dg,ds=ds):
    cm = ds*np.tan(np.radians(dg))
    return cm
def px2dg(px,cm2dg=cm2dg,px2cm=px2cm):
    dg = cm2dg(px2cm(px))
    return dg
def dg2px(dg,cm2px=cm2px,dg2cm=dg2cm):
    px = int(cm2px(dg2cm(dg)))
    return px

# ====================================================================================
# Converting win dimensions to pixels
#winSz = dg2px(winSz)
winSz = grtSize + 2
winOffX = dg2px(winOffX)
winOffY = dg2px(winOffY)
fixSz = dg2px(fixSz)
posCentL = [-winOffX, winOffY]
posCentR = [winOffX, winOffY]
print winSz 
print posCentL 
print posCentR 

# ====================================================================================
# Setup the Window
win = visual.Window(size=dr, fullscr=True, screen=0, allowGUI=False, 
      allowStencil=False, color='grey', blendMode='avg', useFBO=True, units='pix')
# store frame rate of monitor if we can measure it successfully:
frameRate=win.getActualFrameRate()
if frameRate!=None:
    frameDur = 1.0/round(frameRate)
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# ====================================================================================

# Store info about the experiment session
expInfo = {u'session': u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName) # dialogue box
if dlg.OK == False: core.quit()  # user pressed cancel
timeNow = datetime.now()
expInfo['time'] = datetime.now().strftime('%Y-%m-%d_%H%M')
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
if precompileMode:
    precompiledDir = '..' + os.sep + 'precompiledMCs'
dataDir = '..' + os.sep + 'data'
fileName = '%s_p%s_s%s_%s' %(expName, expInfo['participant'], expInfo['session'],
    expInfo['time'])
filePath = dataDir + os.sep + fileName
print filePath

# Condition-related variables
conditionsFilePath = 'cond-files'+os.sep+'cond-'+expName+'.csv' #TEMP
print conditionsFilePath
os.chdir(_thisDir)

# ====================================================================================

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()
instrTextL = visual.TextStim(win, text='Press any key to start', font='Cambria',
                             pos=posCentL, height=dg2px(.65), wrapWidth=dg2px(5),
                             color='white', alignHoriz='center')
instrTextR = visual.TextStim(win, text='Press any key to start', font='Cambria',
                             pos=posCentR, height=dg2px(.65), wrapWidth=dg2px(5),
                             color='white', alignHoriz='center')

# Initialize components for Routine "trial"
trialClock = core.Clock()
moveClock = core.Clock()
maskMoveClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=frameRate, name='ISI')
# circular windows:
winL = visual.Polygon(win, edges=36, size=[winSz, winSz], pos=posCentL,
                      lineWidth=winThickness, lineColor='white')
winR = visual.Polygon(win, edges=36, size=[winSz, winSz], pos=posCentR,
                      lineWidth=winThickness, lineColor='white')
# color masks:
colMaskL = visual.GratingStim(win, size=[grtSize, grtSize], pos=posCentL, opacity=defAlpha,
                              colorSpace='hsv')
colMaskR = visual.GratingStim(win, size=[grtSize, grtSize], pos=posCentR, opacity=defAlpha,
                              colorSpace='hsv')
# direction feedback:
dirFdbkL = visual.Line(win, start=[0,0], end=[0,0], lineColor='white',
                        lineWidth=fdbkThick)
dirFdbkR = visual.Line(win, start=[0,0], end=[0,0], lineColor='white',
                        lineWidth=fdbkThick)
# fixation:
fixL = visual.ShapeStim(win, pos=posCentL, vertices=((0,-fixSz), (0,fixSz), (0,0), 
                                                     (-fixSz,0), (fixSz,0)),
                        lineWidth=.2, closeShape=False, lineColor='white')
fixR = visual.ShapeStim(win, pos=posCentR, vertices=((0,-fixSz), (0,fixSz), (0,0), 
                                                     (-fixSz,0), (fixSz,0)),
                        lineWidth=.2, closeShape=False, lineColor='white')
# pause text:
pauseTextL = visual.TextStim(win, text='Press Spacebar to continue', font='Cambria',
                             alignHoriz='center', pos=posCentL, height=dg2px(.7),
                             wrapWidth=dg2px(3), color='white')
pauseTextR = visual.TextStim(win, text='Press Spacebar to continue', font='Cambria',
                             alignHoriz='center', pos=posCentR, height=dg2px(.7),
                             wrapWidth=dg2px(3), color='white')

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
instructionsComponents.append(instrTextL)
instructionsComponents.append(instrTextR)
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

# ====================================================================================
# Various functions for use in trials:

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.arange(-grtSize/2,grtSize/2)
y = np.arange(-grtSize/2,grtSize/2)
x, y = np.meshgrid(x, y)
R = np.sqrt((x+.5)**2 + (y+.5)**2) # adding .5 ensures symmetry

def combinedMask(fovGap, fovFade, periGap, periFade, R=R):
    fovMask = sigmoid(R * (10./fovFade) - (fovGap * (10./fovFade)) - 5)*2 - 1
    periMask = sigmoid(R * (-10./(periFade)) + 5 + periGap*(10./periFade))*2 - 1
    return fovMask * periMask

# ====================================================================================

#-------Start Routine "instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instrText* updates
    if t >= 0.0 and instrTextL.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrTextL.tStart = t  # underestimates by a little under one frame
        instrTextL.frameNStart = frameN  # exact frame index
        instrTextL.setAutoDraw(True)
        instrTextR.tStart = t  # underestimates by a little under one frame
        instrTextR.frameNStart = frameN  # exact frame index
        instrTextR.setAutoDraw(True)
    
    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
        winL.setAutoDraw(True)
        winR.setAutoDraw(True)
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
    continueRoutine = False  # reverts to True if at least 1 component still running
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
    dirL = 0 #thisTrial['dirL']
    dirR = 0 #thisTrial['dirR']
    #print 'dirL=' + str(dirL) + '; dirR=' + str(dirR)
    vL = thisTrial['vL']
    vR = thisTrial['vR']
    print 'vL=' + str(vL) + '; vR=' + str(vR)
    szL = thisTrial['szL']
    szR = thisTrial['szR']
    print 'szL=' + str(szL) + '; szR=' + str(szR)
    sfL = thisTrial['sfL']
    sfR = thisTrial['sfR']
    print 'sfL=' + str(sfL) + '; sfR=' + str(sfR)
    BvL = thisTrial['BvL']
    BvR = thisTrial['BvR']
    if BvL == 'NA': BvL = .5 # default value
    if BvR == 'NA': BvR = .5
    print 'BvL=' + str(BvL) + '; BvR=' + str(BvR)
    BsfL = thisTrial['BsfL']
    BsfR = thisTrial['BsfR']
    print 'BsfL=' + str(BsfL) + '; BsfR=' + str(BsfR)
    fovGap = thisTrial['fovGap']
    fovFade = thisTrial['fovFade']
    print 'fovGap=' + str(fovGap) + '; fovFade=' + str(fovFade)
    periGap = thisTrial['periGap']
    periFade = thisTrial['periFade']
    print 'periGap=' + str(periGap) + '; periFade=' + str(periFade)
    fixCross = thisTrial['fixCross']
    flickRate = thisTrial['flickRate']
    
    # Setting starting trial colors:
    sat = thisTrial['colStart'] # alpha value
    colStep = thisTrial['colStep'] # alpha step
    print 'sat=' + str(sat) + '; colStep=' + str(colStep)
    colOdd = [150,1,1] # green
    colEven = [330,sat,1] # red is adjusted and is assigned to gratings in even frames

    # initiating the gratings
    if precompileMode:
        grtL = np.load(precompiledDir + os.sep + 'mc_' + '{0:.1f}'.format(vL) +
               '_sf' + str(sfL) + '_bsf' + str(BsfL) + '_bv' + str(BvL) + 
               '_sz' + str(szL) + '.npy')
        grtR = np.load(precompiledDir + os.sep + 'mc_' + '{0:.1f}'.format(vR) +
               '_sf' + str(sfR) + '_bsf' + str(BsfR) + '_bv' + str(BvR) +
               '_sz' + str(szR) + '.npy')
    else:
        fx, fy, ft = mc.get_grids(szL, szL, nFrames)
        grtCol = mc.envelope_color(fx, fy, ft)
        grtL = 2*mc.rectif(mc.random_cloud(grtCol * 
               mc.envelope_gabor(fx, fy, ft, sf_0=sfL, B_sf=BsfL, B_V=BvL,
               V_X=vL, B_theta=np.inf))) - 1
        fx, fy, ft = mc.get_grids(szR, szR, nFrames)
        grtCol = mc.envelope_color(fx, fy, ft)
        grtR = 2*mc.rectif(mc.random_cloud(grtCol * 
               mc.envelope_gabor(fx, fy, ft, sf_0=sfR, B_sf=BsfR, B_V=BvR,
               V_X=vR, B_theta=np.inf))) - 1

    # Creating a mask, which is fixed for a given trial:
    curMask = combinedMask(fovGap, fovFade, periGap, periFade)

    # Using the mask to assign both the greyscale values and the mask for our color masks:
    colMaskL.tex = (curMask + 1)/2
    colMaskL.mask = curMask
    colMaskR.tex = (curMask + 1)/2
    colMaskR.mask = curMask

    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    tMaskMove = 0
    qnResp = 0
    endTrialKeyPressed = False
    behRespRecorded = False
    key_pause = False
    # update component parameters for each repeat
    key_arrow = event.BuilderKeyResponse()  # create an object of type KeyResponse
    key_arrow.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(winL)
    trialComponents.append(winR)
    trialComponents.append(key_arrow)
    trialComponents.append(pauseTextL)
    trialComponents.append(pauseTextR)
    trialComponents.append(ISI)
    trialComponents.append(fixL)
    trialComponents.append(fixR)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        
        # get current time and set some frame variables:
        t = trialClock.getTime()
        frameN = frameN + 1 # number of completed frames (0 is the first frame)
        oddFrame = (frameN//(nFrames/flickRate))%2 # yields 0 when even; 1 when odd

        # update/draw components on each frame
        
        # *winL* updates
        if winL.status == NOT_STARTED:
            # keep track of start time/frame for later
            winL.tStart = t  # underestimates by a little under one frame
            winL.frameNStart = frameN  # exact frame index
            winL.setAutoDraw(True)
            winL.status = STARTED
        
        # *winR* updates
        if winR.status == NOT_STARTED:
            # keep track of start time/frame for later
            winR.tStart = t  # underestimates by a little under one frame
            winR.frameNStart = frameN  # exact frame index
            winR.setAutoDraw(True)
            winR.status = STARTED

        # stimulus presentation:
        if not endTrialKeyPressed:
            # Checking if the frame is "even" or "odd" to deside whether to present red or blue grat:
            if oddFrame:
                curCol = colOdd
            else: # if even frame, adjust the color of red grating:
                curCol = [330,sat,1]
            # Drawing the gratings:
            #stimL = visual.GratingStim(win, tex=grtL[:,:,frameN%nFrames], size=(grtSize,grtSize),
            stimL = visual.GratingStim(win, tex=grtL[:,:,0], size=(grtSize,grtSize),
                pos=posCentL, interpolate=False, mask=curMask, ori=90+dirL)
            stimL.draw()
            stimR = visual.GratingStim(win, tex=grtR[:,:,0], size=(grtSize,grtSize),
                pos=posCentR, interpolate=False, mask=curMask, ori=90+dirR)
            stimR.draw()
            # Drawing the color masks:
            colMaskL.color = curCol
            colMaskL.draw()
            colMaskR.color = curCol
            colMaskR.draw()
            # Drawing the fixation cross:
            if fixCross:
                fixL.draw()
                fixR.draw()
        
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
        # registering response at the end of the trial for short trials:
        if key_arrow.status == STARTED and not endTrialKeyPressed:
            theseKeys = event.getKeys(keyList=['up','down','space'])
            if len(theseKeys) > 0:
                if 'up' in theseKeys:
                    print '"up" key is pressed'
                    # adjusting the red intensity/saturation:
                    sat = sat + colStep
                    ## adjusting the red alpha-value:
                    #av = av + colStep
                elif 'down' in theseKeys:
                    print '"down" key is pressed'
                    # adjusting the red intensity/saturation:
                    sat = sat - colStep
                    ## adjusting the red alpha-value:
                    #av = av - colStep
                elif 'space' in theseKeys:
                    print 'equiluminance set at ' + str(sat)
                    totFrames = frameN # how long it took for the viewer to adjust
                    endTrialKeyPressed = True

        # pause text and data exporting
        if endTrialKeyPressed:
            if not behRespRecorded: # a flag for data recording
                # Recording the responses:
                behRespRecorded = True
                pauseTextL.setAutoDraw(True)
                pauseTextR.setAutoDraw(True)
                dT = pd.DataFrame({'expName': expName,
                                   'time': expInfo['time'],
                                   'participant': expInfo['participant'],
                                   'session': expInfo['session'],
                                   'trialN': nDone,
                                   'dirL': dirL, 'dirR': dirR,
                                   'vL': vL, 'vR': vR, 'szL': szL, 'szR': szR,
                                   'sfL': sfL, 'sfR': sfR, 'BvL': BvL, 'BvR': BvR,
                                   'BsfL': BsfL, 'BsfR': BsfR,
                                   'colOdd': str(colOdd), 'colEven': str(colEven), 'sat': sat,
                                   'fovGap': fovGap, 'fovFade': fovFade,
                                   'periGap': periGap, 'periFade': periFade,
                                   'totFrames': [totFrames]}) # how long it took for viewer to adj
                # to preserve the column order:
                dataCols = ['expName', 'time', 'participant', 'session', 'trialN',
                            'dirL', 'dirR', 'vL', 'vR', 'szL', 'szR', 'sfL', 'sfR',
                            'tfL', 'tfR', 'BsfL', 'BsfR', 'colOdd', 'colEven', 'sat',
                            'fovGap', 'fovFade', 'periGap', 'periFade', 'totFrames']
                if nDone == 1:
                    df = dT
                else:
                    df = pd.concat([df,dT])
                # Recording the data to a csv file:
                df.to_csv(dataFileName, index=False, columns=dataCols)
                print 'wrote the data set to ' + dataFileName
            if 'space' in event.getKeys(keyList=['space']):
                print 'spacebar pressed - continuing to the next trial'
                pauseTextL.setAutoDraw(False)
                pauseTextR.setAutoDraw(False)
                key_pause = True

        # *ISI* period
        if ISI.status == NOT_STARTED and endTrialKeyPressed and key_pause:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            fixL.setAutoDraw(True)
            fixR.setAutoDraw(True)
            ISI.start(ISIduration)
        #one frame should pass before updating params and completing
        elif ISI.status == STARTED and t >= (ISI.tStart + ISIduration): 
            fixL.setAutoDraw(False)
            fixR.setAutoDraw(False)
            ISI.complete() #finish the static period
            # stopping eye-tracking recording:
            if et:
                elEndRec(el)
            continueRoutine = False
        
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
            if et:
                elEndRec(el)
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

if et:
    # File transfer and cleanup!
    pl.endRealTimeMode()
    el.setOfflineMode()						  
    pl.msecDelay(600) 

    #Close the file and transfer it to Display PC
    el.closeDataFile()
    el.receiveDataFile(edfFileName, edfFileName)
    el.close()

print "finished the experiment"

win.close()
core.quit()
