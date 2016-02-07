#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

SIZE = 1024
GRAINS = 1024
ONE = 1./SIZE

LEAP = 1

BACK = [1,1,1,1]
FRONT = [0,0,0,5]



def main():

  from modules.sand import Sand
  from matplotlib.pyplot import figure
  from matplotlib.pyplot import ion
  from matplotlib.pyplot import clf
  from matplotlib.pyplot import plot
  from numpy.random import random
  from matplotlib.pyplot import draw
  from matplotlib.pyplot import xlim
  from matplotlib.pyplot import ylim
  from matplotlib.pyplot import tight_layout
  from matplotlib.pyplot import imshow


  sand = Sand(SIZE)

  sand.spawn(GRAINS)

  figure(0)
  ion()


  img = imshow(
    random((SIZE,SIZE)),
    cmap='Greys',
    interpolation='nearest'
  )

  for i in xrange(1000000):

    sand.step()

    if sand.i % LEAP == 0:
      print(sand.i)

      # clf()
      vals = sand.get_normalized_sand(dbg=True)
      img.set_data(vals)
      # for g in sand.get_grains():
        # x,y = g.get_pos()
        # plot(x, y, 'ro')

      # xlim([0,1])
      # ylim([0,1])
      tight_layout()
      draw()


if __name__ == '__main__':

    main()

