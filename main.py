#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

SIZE = 1024
ONE = 1./SIZE

LEAP = 10

BACK = [1,1,1,1]
FRONT = [0,0,0,5]



def main():

  from modules.sand import Sand
  # from time import sleep
  # from matplotlib import pyplot as plt
  from matplotlib.pyplot import figure
  from matplotlib.pyplot import ion
  from matplotlib.pyplot import draw
  from matplotlib.pyplot import imshow
  from matplotlib.pyplot import tight_layout


  sand = Sand(SIZE)

  figure(0)
  ion()


  vals = sand.get_normalized_sand(dbg=True).reshape((SIZE,-1))
  img = imshow(
    1.0-vals,
    cmap='Greys',
    interpolation='nearest'
  )

  for i in xrange(1000000):

    sand.step()

    if sand.i % LEAP == 0:
      print(sand.i)

      vals = sand.get_normalized_sand(dbg=False).reshape((SIZE,-1))
      img.set_data(1.0-vals)
      tight_layout()
      draw()


if __name__ == '__main__':

    main()

