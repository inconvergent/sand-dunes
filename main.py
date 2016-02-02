#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from itertools import product

SIZE = 512
ONE = 1./SIZE

LEAP = 100

BACK = [1,1,1,1]
FRONT = [0,0,0,5]


def show(sand, render):

  if sand.i % LEAP != 0:
    return

  size = sand.size
  one = sand.one
  s = sand.get_normalized_sand()

  ctx = render.ctx
  set_rgb = ctx.set_source_rgb
  rect = ctx.rectangle
  fill = ctx.fill
  for i,j in product(xrange(size), repeat=2):
    set_rgb(*[s[i*size+j]]*3)
    x = i*one
    y = j*one
    rect(i*one,j*one,x+one,y+one)
    fill()

def main():

  import gtk
  from render.render import Animate
  from modules.sand import Sand

  sand = Sand(SIZE)

  def wrap(render):

    sand.step()
    show(sand, render)

    return True

  render = Animate(SIZE, BACK, FRONT, wrap)

  gtk.main()



if __name__ == '__main__':

  if False:

    import pyximport
    pyximport.install()
    import pstats, cProfile

    fn = './profile/profile'
    cProfile.runctx("main()", globals(), locals(), fn)
    p = pstats.Stats(fn)
    p.strip_dirs().sort_stats('cumulative').print_stats()

  else:

    main()

