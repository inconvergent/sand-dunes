#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

SIZE = 200
ONE = 1./SIZE

LEAP = 20

BACK = [1,1,1,1]
FRONT = [0,0,0,5]


def main():

  from matplotlib import pyplot as plt
  from modules.sand import Sand
  from time import sleep

  sand = Sand(SIZE)

  # plt.ion()
  # plt.figure()

  # img = plt.imshow(
    # sand.get_normalized_sand().reshape((SIZE,-1)),
    # cmap='Greys',
    # interpolation='nearest'
  # )
  # plt.show()

  for i in xrange(1000000):

    sand.step()

    if sand.i % LEAP == 0:

      print(sand.i)

      # img.set_data(
        # sand.get_normalized_sand().reshape((SIZE,-1))
      # )
      # sleep(0.00001)

      plt.imshow(
        sand.get_normalized_sand(dbg=True).reshape((SIZE,-1)),
        cmap='Greys',
        interpolation='nearest'
      )
      plt.show()
      # plt.draw()


if __name__ == '__main__':

    main()

