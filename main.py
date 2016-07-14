#!/usr/bin/python3
# -*- coding: utf-8 -*-


SIZE = 512
IMG = './img/x512-text.png'
GRAINS = 500
ONE = 1./SIZE

LEAP = 10000

BACK = [1,1,1,1]
FRONT = [0,0,0,5]

ANGLE_STP = 0.001

def get_initial(img):
  from numpy.random import random
  from scipy.ndimage.filters import gaussian_filter
  from modules.helpers import get_img_as_rgb_array

  initial = get_img_as_rgb_array(img)[:,:,0].squeeze()
  initial *= 200
  initial += 50
  initial += random(initial.shape)*10.0

  gaussian_filter(
    initial,
    2,
    output=initial,
    order=0,
    mode='mirror'
    )

  return initial.astype('int')


def main():

  from modules.dunes import Dunes
  from sand import Sand
  from fn import Fn

  # from numpy import dstack

  initial = get_initial(IMG)
  dunes = Dunes(
      SIZE,
      initial,
      grains=GRAINS,
      angle_stp=ANGLE_STP
      )

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  try:
    while True:
      dunes.step()

      if dunes.i % LEAP == 0:
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

