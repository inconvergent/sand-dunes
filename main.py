#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import zeros
from numpy import dstack


SIZE = 1000
IMG = './img/gen.png'
ONE = 1./SIZE

LEAP = 50000
PROB = 0.3

DELTA = 10

BACK = [1,1,1,1]
FRONT = [0,0,0,5]

def get_initial_rnd():
  from scipy.ndimage.filters import gaussian_filter
  from numpy.random import random
  initial = random((SIZE,SIZE))*15
  gaussian_filter(
    initial,
    2,
    output=initial,
    order=0,
    mode='mirror'
    )

  return initial.astype('int')

def get_initial(img):
  from modules.helpers import get_img_as_rgb_array

  initial = 1.0 - get_img_as_rgb_array(img)[:,:,0].squeeze()
  initial *= 20

  return initial.astype('int')

def save_shadow_map(dunes, sand):
  bw = zeros((SIZE,SIZE),'float')
  shadow = zeros((SIZE,SIZE),'float')
  dunes.get_normalized_sand(bw)
  dunes.get_shadow(shadow)
  rgb = dstack((zeros(bw.shape,'float'),bw,1.0-shadow))
  sand.set_bg_from_rgb_array(rgb)
  sand.write_to_png('shadow.png')


def main():

  from dunes import Dunes
  from sand import Sand
  from fn import Fn
  from time import time

  initial = get_initial(IMG)
  # initial = get_initial_rnd()
  bw = zeros(initial.shape,'float')
  shadow = zeros(initial.shape,'float')

  dunes = Dunes(initial, DELTA, PROB)

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  try:
    while True:

      t0 = time()
      itt = dunes.steps(LEAP)
      print(itt, time()-t0)
      dunes.get_normalized_sand(bw)
      # bw *= 0.8
      # sand.set_bg_from_bw_array(bw)
      # dunes.get_shadow(shadow)
      # rgb = dstack((bw,bw,shadow))
      # sand.set_bg_from_rgb_array(rgb)
      sand.set_bg_from_bw_array(bw)
      name = fn.name()
      sand.write_to_png(name)

  except KeyboardInterrupt:
    pass
  #

if __name__ == '__main__':
  main()

