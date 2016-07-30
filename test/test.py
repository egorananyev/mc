import psychopy
import MotionClouds as mc
import numpy as np
import vispy
from vispy import scene
#from vispy.visuals.transforms import STTransform,MatrixTransform

# define Fourier domain
fx, fy, ft = mc.get_grids(mc.N_X, mc.N_Y, mc.N_frame)
# define an envelope
envelope = mc.envelope_gabor(fx, fy, ft, V_X=1., V_Y=0., B_V=.1,
    sf_0=.15, B_sf=.1, theta=0., B_theta=np.pi/8, alpha=1.)
# Visualize the Fourier Spectrum
#mc.visualize(envelope)
mc.figures(envelope,'test')
#mc.in show video('test')
