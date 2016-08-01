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
import MotionClouds as mc
# allScrs = pyglet.window.get_platform().get_default_display().get_screens()
# print allScrs

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Output directory:
precompiledDir = '..' + os.sep + 'precompiledMCs'
if not os.path.exists(precompiledDir):
    os.makedirs(precompiledDir)

# Input directory:
expName = 'mcv' # Experiment name
conditionsFilePath = 'cond-files'+os.sep+'cond-mcv'+'.csv'
print conditionsFilePath

# Dimension variables:
windowSize = 7
# viewingDist = 53.7
# monitorWidth = 47.6
# monitorHeight = 298
# monitorXpx = 1680
# monitorYpx = 1050
dimMulti = 33

# Setting up the conditions:
condList = data.importConditions(conditionsFilePath)
grtList = []
for thisCondition in condList:
    grtName = expName + '_' + str(thisCondition['vL'])
    # print grtName
    if grtName not in grtList:
        grtList.append(grtName)
        name_ = precompiledDir + os.sep + grtName
        # grating characteristics:
        thisSf = thisCondition['sfLx']
        thisBsf = thisCondition['BsfL']
        thisV = thisCondition['vL']
        szX = int(windowSize*dimMulti) # assuming 1680x1050, 476x298, dist 53.7
        szY = szX
        nFrames = 60 #*thisCondition['trialT']
        # compiling the gratings:
        fx, fy, ft = mc.get_grids(szX, szY, nFrames)
        print 'starting color for ' + name_
        grtCol = mc.envelope_color(fx, fy, ft)
        print 'starting envelope for ' + name_
        z = mc.envelope_gabor(fx, fy, ft, sf_0=thisSf, B_sf=thisBsf, V_X=thisV, B_theta=np.inf)
        print 'starting cloud for ' + name_
        zcl = mc.random_cloud(grtCol * z)
        grtL = 2*mc.rectif(zcl) - 1
        # saving the gratings:
        np.save(name_, grtL)
        # mc.figures(grtL, name_, vext='.mkv')
        print 'precompiled ' + name_
