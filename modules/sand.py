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

INC = 1


class Grain(object):

  def __init__(self, sand, xy):
    self.sand = sand
    self.trail = xy

    self.size = sand.size
    self.stp = sand.stp
    self.angle_stp = sand.angle_stp
    self.one = sand.one

  def get_pos(self):
    return self.trail.flatten()

  def get_ind(self):
    return (self.trail*self.size).astype('int').flatten()

  def reselect(self):

    size = self.size
    i,j = self.get_ind()
    self.sand.sand[i,j] += INC

    while True:
      new_xy = random(2)
      ni,nj = (size*new_xy).astype('int').flatten()
      if self.sand.sand[ni,nj]>=INC:
        self.trail = new_xy
        self.sand.sand[ni,nj] -= INC
        break

  def step(self):

    size = self.size
    xy = self.trail
    dx = self.sand.dx

    fi,fj = (size*(xy+dx)).astype('int').flatten()
    bi,bj = (size*(xy-dx)).astype('int').flatten()

    slope = 0
    sand = self.sand.sand

    try:
      slope = sand[fi,fj] - sand[bi,bj]
    except IndexError:
      pass

    xy_new = xy+dx

    up_mask = xy_new>=1.0
    dwn_mask = xy_new<=0.0
    if dwn_mask.any():
      xy_new[dwn_mask] += 1
    if up_mask.any():
      xy_new[up_mask] %= 1


    if (slope>0 and random()<0.7) or (random()<0.2):
      self.reselect()
      return True

    self.trail = xy_new
    x,y = self.get_ind()

    # TODO: if alive
    return True


class Sand(object):

  def __init__(self, size, angle_stp=0.01):
    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp

    self.stp = self.one
    self.sand = zeros((size,size), 'float')
    self.sand[200-50:200+50,:] = 20 *INC*random((100,size))

    self.grains = []

    self.a = 0.3*TWOPI
    self.__set_direction()
    self.i = 1

  def spawn(self, n=1):
    xys = random(size=(n,2))
    for xy in xys:
      self.grains.append(Grain(self, xy.flatten()))

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
    # self.a += (1.0-2.0*random())*self.angle_stp
    a = self.a
    self.dx = array([cos(a), sin(a)], 'float')*self.stp

  def step(self):
    self.i += 1
    self.__set_direction()

    for g in self.grains:
      g.step()

    return len(self.grains)>0

