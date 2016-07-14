#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import zeros


SIZE = 512
IMG = './img/x512.png'
ONE = 1./SIZE

LEAP = 10000

BACK = [1,1,1,1]
FRONT = [0,0,0,5]


def get_initial(img):
  from numpy.random import random
  from modules.helpers import get_img_as_rgb_array

  # initial = zeros((SIZE,SIZE), 'float')
  # initial[0,0] = 1
  # initial[1,0] = 1
  # initial[1,3] = 1
  # initial[2,0] = 2
  # initial[2,1] = 2
  # initial[10,3:] = 1

  initial = get_img_as_rgb_array(img)[:,:,0].squeeze()
  initial *= 20
  initial += random(initial.shape)*15

  # from scipy.ndimage.filters import gaussian_filter
  # gaussian_filter(
  #   initial,
  #   2,
  #   output=initial,
  #   order=0,
  #   mode='mirror'
  #   )

  return initial.astype('int')

def save_shadow_map(dunes, sand):
  from numpy import dstack
  bw = dunes.get_normalized_sand()
  shadow = dunes.get_shadow()
  rgb = dstack((zeros(bw.shape,'float'),bw,1.0-shadow))
  sand.set_bg_from_rgb_array(rgb)
  sand.write_to_png('shadow.png')


def main():

  from modules.dunes import Dunes
  from sand import Sand
  from fn import Fn

  initial = get_initial(IMG)
  print(initial)
  print()

  dunes = Dunes(initial)

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  save_shadow_map(dunes, sand)

  try:
    while True:

      dunes.steps(steps=LEAP)
      print(dunes.i)
      bw = dunes.get_normalized_sand()
      # rgb = dstack((bw,bw,bw))
      sand.set_bg_from_bw_array(bw)
      name = fn.name()
      sand.write_to_png(name)

  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  main()

