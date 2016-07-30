import psychopy
import numpy as np
import vispy
from vispy import scene
import MotionClouds as mc
print(dir(mc))
#from vispy.visuals.transforms import STTransform,MatrixTransform

# define Fourier domain
fx, fy, ft = mc.get_grids(mc.N_X, mc.N_Y, mc.N_frame)
# define an envelope
envelope = mc.envelope_gabor(fx, fy, ft, V_X=1., V_Y=0., B_V=.1,
    sf_0=.15, B_sf=.1, theta=0., B_theta=np.pi/8, alpha=1.)
# Visualize the Fourier Spectrum
mc.visualize(envelope)
mc.figures(envelope,'test')
movie=mc.random_cloud(envelope)
movie=mc.rectif(movie)
name = 'testmc'
mc.cube(movie, name=name+'_cube')
mc.anim_save(movie, name, display=True, vext='.mp4')
