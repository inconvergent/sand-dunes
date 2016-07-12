#!/usr/bin/python3
# -*- coding: utf-8 -*-


SIZE = 900
GRAINS = 1000
ONE = 1./SIZE

LEAP = 5000

INC = 1.0

BACK = [1,1,1,1]
FRONT = [0,0,0,5]



def main():

  from modules.dunes import Dunes
  from sand import Sand
  from fn import Fn


  dunes = Dunes(SIZE, grains=GRAINS, angle_stp=0.0, inc=INC)

  sand = Sand(SIZE)
  sand.set_rgba(FRONT)
  fn = Fn(prefix='./res/', postfix='.png')

  try:
    for i in range(1000000):

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

