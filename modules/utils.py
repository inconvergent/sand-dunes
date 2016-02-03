# -*- coding: utf-8 -*-

from __future__ import print_function

def get_dens_from_img(fn):

  from scipy.ndimage import imread

  return imread(fn)/255.

