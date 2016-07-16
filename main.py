#!/usr/bin/python3
# -*- coding: utf-8 -*-

from numpy import zeros


SIZE = 512
IMG = './img/gen.png'
ONE = 1./SIZE

LEAP = 50000
PROB = 0.3

DELTA = 10

BACK = [1,1,1,1]
FRONT = [0,0,0,5]



def main():

  from dunes import Dunes
  from sand import Sand
  from fn import Fn
  from time import time


  # from modules.helpers import get_initial
  # initial = get_initial(IMG)

  from modules.helpers import get_initial_rnd
  initial = get_initial_rnd(SIZE, n=2)
  bw = zeros(initial.shape,'float')

  dunes = Dunes(initial, DELTA, PROB)

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  try:
    while True:
      t0 = time()
      itt = dunes.steps(LEAP)
      print(itt, time()-t0)
      dunes.get_normalized_sand_limit(bw, 10)
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


if __name__ == '__main__':
  main()

