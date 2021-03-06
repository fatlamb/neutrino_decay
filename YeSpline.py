import numpy as np
import scipy as sp
from scipy.integrate import ode
import matplotlib.pyplot as plt
from numpy import linalg as LA
from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline

import dill as pickle

from scipy.ndimage.filters import gaussian_filter1d as gausfilt
import random
import cmath
import math

## A simple function defining a piecewise electron fraction as a function of 
# earth radius.
def ye(x):
    if x <= 0.5475:
        return 0.4656
    else:
        return 0.4957

## A function which smooths the piecewise profile from ye() and fits a spline.
# Smooths the electron fraction profile using a gaussian 
# convolution to avoid trouble with the numerical solver in DeSolve encountering
# discontinuities in the potential. A UnivariateSpline is fit to the smoothed profile.
# The script containing this function is executable, and will pickle the spline and
# write it to ye_spline.p.
# @return the fit spline.

def YeSpline():
    """
    Returns a cubic spline of gaussian-smoothed density profile.
    """
    dist = np.linspace(0, 1.2, 12000, endpoint=True)
    dense = np.zeros(len(dist))
    for x in range(0, len(dist)):
        dense[x] = ye(dist[x])

    smooth = gausfilt(dense, 10)
    smoothfunc = interp1d(dist, smooth, kind='linear')
    smalldense = np.zeros(1200)
    smalldist = np.linspace(0, 1.2, 1200, endpoint=True)
    for x in range(0, len(smalldist)):
        smalldense[x] = smoothfunc(smalldist[x])
    #func = interp1d(smalldist, smalldense, kind='cubic') 
    func = InterpolatedUnivariateSpline(smalldist, smalldense, k=3)
    return func


ye_spline=YeSpline()
pickle.dump( ye_spline, open( "ye_spline.p", "wb" ) )

