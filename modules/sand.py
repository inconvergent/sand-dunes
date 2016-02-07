# -*- coding: utf-8 -*-

from __future__ import print_function

from numpy import pi
from numpy.random import random
from numpy import cos
from numpy import sin
from numpy import array
from numpy import zeros
from numpy import logical_or
from numpy.linalg import norm


TWOPI = pi*2.0


class Grain(object):

  def __init__(self, sand, xy):
    self.sand = sand
    self.trail = [xy]

    self.size = sand.size
    self.stp = sand.stp
    self.angle_stp = sand.angle_stp
    self.one = sand.one

  def get_pos(self):
    return self.trail[-1]

  def get_ind(self):
    return (self.trail[-1]*self.size).astype('int').flatten()

  def step(self):

    size = self.size
    xy = self.trail[-1]
    dx = self.sand.dx

    bx,by = (size*(xy-dx)).astype('int').flatten()
    fx,fy = (size*(xy+dx)).astype('int').flatten()

    slope = 0
    sand = self.sand.sand

    try:
      slope = sand[fx,fy] - sand[bx,by]
    except IndexError:
      pass

    if slope<0:
      beta = 10.0*random()
    else:
      beta = random()

    xy_new = xy+dx*(1.0+beta)

    # print(norm(dx*size), norm(size*dx*(1.0+beta)))

    if logical_or(xy_new>1.0, xy_new<0).any():
      xy_new = random(size=(1,2))

    self.trail.append(xy_new)
    x,y = self.get_ind()
    self.sand.sand[x,y] += 6

    # TODO: if alive
    return True


class Sand(object):

  def __init__(self, size, angle_stp=0.01):
    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp

    self.stp = self.one
    # self.sand = random((size,size))*1
    self.sand = random((size,size))*100
    # self.sand = zeros((size,size), 'float')

    self.grains = []

    self.a = 0.3*TWOPI
    self.__set_direction()
    self.i = 1

  def spawn(self, n=1):
    xys = random(size=(n,2))
    for xy in xys:
      self.grains.append(Grain(self, xy))

  def get_sand(self):
    return self.s

  def get_grains(self):
    return self.grains

  def get_normalized_sand(self, dbg=False):
    sand = self.sand
    flat = sand.reshape((-1,1))

    mi = flat.min()
    ma = flat.max()

    if dbg:
      print(mi, ma)

    return (sand[:,:]-mi)/(ma-mi)

  def __set_direction(self):
    self.a += (1.0-2.0*random())*self.angle_stp
    a = self.a
    self.dx = array([cos(a), sin(a)], 'float')*self.stp

  def step(self):
    self.i += 1
    self.__set_direction()

    for g in self.grains:
      g.step()

    return len(self.grains)>0

