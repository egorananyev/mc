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

nFrames = 60 #*thisCondition['trialT']

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Output directory:
precompiledDir = '..' + os.sep + 'precompiledMCs'
if not os.path.exists(precompiledDir):
    os.makedirs(precompiledDir)

# Input directory:
conditionsFilePath = 'cond-files' + os.sep + 'cond-mcv_annu.csv'
print conditionsFilePath

# Setting up the conditions:
condList = data.importConditions(conditionsFilePath)
grtList = []
for thisCondition in condList:
    # grating name:
    grtSz = thisCondition['szL']
    thisSf = thisCondition['sfL']
    thisBsf = thisCondition['BsfL']
    if thisCondition['dirL'] < 0: # this means clockwise or CCW motion
        thisV = 0
    else: # translational motion
        thisV = thisCondition['vL']
    thisBv = thisCondition['BvL']
    grtName = precompiledDir + os.sep + 'mc_' + str(thisV) + '_sf' + str(thisSf) + \
        '_bsf' + str(thisBsf) + '_bv' + str(thisBv) + '_sz' + str(grtSz)
    if grtName not in grtList:
        grtList.append(grtName)
        # compiling the gratings:
        szX = grtSz
        szY = szX
        fx, fy, ft = mc.get_grids(szX, szY, nFrames)
        grtCol = mc.envelope_color(fx, fy, ft)
        z = mc.envelope_gabor(fx, fy, ft, sf_0=thisSf, B_sf=thisBsf,
            V_X=thisV, B_V=thisBv, B_theta=np.inf)
        zcl = mc.random_cloud(grtCol * z)
        grtL = 2*mc.rectif(zcl) - 1
        # saving the gratings:
        np.save(grtName, grtL)
        # mc.figures(grtL, grtName, vext='.mkv')
        print 'precompiled ' + grtName
