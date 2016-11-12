import numpy as np
import MotionClouds as mc

# DEBUG:
#import psychopy
#import vispy
#from vispy import scene
#print(dir(mc))
#from vispy.visuals.transforms import STTransform,MatrixTransform

# params:
sf0 = 0.025
bsf = .01
theta = 0
bTheta = 3.14
vX = 0
vY = 0
bV = .001

# define Fourier domain
fx, fy, ft = mc.get_grids(mc.N_X, mc.N_Y, mc.N_frame)
# define an envelope
envelope = mc.envelope_gabor(fx, fy, ft, V_X=vX, V_Y=vY, B_V=bV,
    sf_0=sf0, B_sf=bsf, theta=theta, B_theta=bTheta, alpha=1.)
# Visualize the Fourier Spectrum
mc.visualize(envelope)
mc.figures(envelope,'test')
movie=mc.random_cloud(envelope)
movie=mc.rectif(movie)
name = 'sf' + str(sf0) + '_bsf' + str(bsf) + '_vX' + str(vX) + '_vY' + str(vY) + '_bV' + str(bV) + '_th' + str(theta) + '_bTh' + str(bTheta)
print name
mc.cube(movie, name=name+'_cube')
mc.anim_save(movie, name, display=True, vext='.mp4')
