#!/usr/bin/python3
# -*- coding: utf-8 -*-


SIZE = 512
GRAINS = 100
ONE = 1./SIZE

LEAP = 50000

INC = 1.0

BACK = [1,1,1,1]
FRONT = [0,0,0,5]

def get_initial(img):
  from numpy.random import random
  from scipy.ndimage.filters import gaussian_filter
  from modules.helpers import get_img_as_rgb_array

  initial = get_img_as_rgb_array(img)[:,:,0].squeeze()
  initial += random(initial.shape)*0.01
  initial *= 100

  gaussian_filter(
    initial,
    0.2,
    output=initial,
    order=0,
    mode='mirror'
    )

  return initial


def main():

  from modules.dunes import Dunes
  from sand import Sand
  from fn import Fn

  initial = get_initial('./img/x512.png')
  dunes = Dunes(SIZE, initial, grains=GRAINS, angle_stp=0.0, inc=INC)

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  try:
    while True:
      dunes.step()

      if dunes.i % LEAP == 0:
        print(dunes.i)
        bw = dunes.get_normalized_sand(dbg=True)
        sand.set_bg_from_bw_array(bw)
        name = fn.name()
        sand.write_to_png(name)

  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  main()

