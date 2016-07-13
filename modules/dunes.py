# -*- coding: utf-8 -*-

from numpy import pi
from numpy.random import random
from numpy import cos
from numpy import sin
from numpy import array
from numpy import zeros

from numpy import logical_not
from numpy import logical_or

TWOPI = pi*2.0


class Dunes(object):

  def __init__(
      self,
      size,
      initial,
      grains=10,
      angle_stp=0.01,
      inc=1.0
      ):
    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp
    self.grains = grains
    self.inc = inc

    self.stp = self.one
    self.sand = zeros((size,size), 'float')
    self.sand[:,:] = initial
    self.xy = random(size=(grains,2))

    self.h = self.one*2

    self.a = pi*0.3
    self.__set_direction()
    self.i = 1

  def get_sand(self):
    return self.sand

  def get_normalized_sand(self, dbg=False):
    sand = self.sand
    flat = sand.reshape((-1,1))

    mi = flat.min()
    ma = flat.max()

    if dbg:
      print(mi, ma)

    return (sand-mi)/(ma-mi)

  def __set_direction(self):
    self.a += (1.0-2.0*random())*self.angle_stp
    a = self.a
    self.dx = array([cos(a), sin(a)], 'float')*self.stp

  def __get_slope(self):
    size = self.size
    sand = self.sand
    xy = self.xy
    dx = self.dx
    fij = (((size*(xy+dx))+size)%size).astype('int')
    bij = (((size*(xy-dx))+size)%size).astype('int')
    slope = sand[fij[:,0],fij[:,1]] - sand[bij[:,0],bij[:,1]]
    return slope

  def step(self):
    self.i += 1
    size = self.size

    self.__set_direction()
    slope = self.__get_slope()

    stopping = logical_or(slope>=0,random(slope.shape)>0.9)

    ij = (self.xy[stopping,:]*self.size).astype('int')

    self.sand[ij[:,0],ij[:,1]] += self.inc
    reselect_num = stopping.sum()

    new_xy = random((reselect_num, 2))
    nij = (size*new_xy).astype('int')
    self.xy[stopping,:] = new_xy
    self.sand[nij[:,0], nij[:,1]] -= self.inc


    continuing = logical_not(stopping)
    self.xy[continuing,:] = (self.xy[continuing,:]+self.dx)%1.0

