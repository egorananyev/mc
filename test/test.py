import numpy as np
import MotionClouds as mc

# DEBUG:
#import psychopy
#import vispy
#from vispy import scene
#print(dir(mc))
#from vispy.visuals.transforms import STTransform,MatrixTransform

# params:
sf0 = 0.1
bsf = .05
vX = 9.6
vY = 0
bV = .5
theta = 60
bTheta = 1.27 #4/3.14

# define Fourier domain
fx, fy, ft = mc.get_grids(mc.N_X, mc.N_Y, 10) #mc.N_frame)
# define an envelope
envelope = mc.envelope_gabor(fx, fy, ft, V_X=vX, V_Y=vY, B_V=bV,
    sf_0=sf0, B_sf=bsf, theta=theta, B_theta=bTheta, alpha=1.)
# Visualize the Fourier Spectrum
#mc.visualize(envelope)
#mc.figures(envelope,'test')
movie=mc.random_cloud(envelope)
movie=mc.rectif(movie)
name = 'sf' + str(sf0) + '_bsf' + str(bsf) + '_vX' + str(vX) + '_vY' + str(vY) + '_bV' + str(bV) + '_th' + str(theta) + '_bTh' + str(bTheta)
print name
mypath = '/c/Users/Egor/Dropbox/Projects/mc/mc/test'
#mc.cube(movie, name=name+'_cube')
mc.anim_save(movie, name, display=False, vext='.mp4') #prev .mp4
