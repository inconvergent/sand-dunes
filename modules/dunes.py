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
      angle_stp=0.01
      ):
    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp
    self.grains = grains

    self.stp = self.one
    self.sand = zeros((size,size), 'int')
    self.sand[:,:] = initial
    self.xy = random(size=(grains,2))

    self.h = self.one*2

    self.a = pi*0.3
    self._set_direction()
    self.i = 1

  def get_sand(self):
    return self.sand

  def get_normalized_sand(self):
    sand = self.sand.astype('float')
    flat = sand.reshape((-1,1))

    mi = flat.min()
    ma = flat.max()
    print(mi, ma)
    return (sand-mi)/(ma-mi)

  def _set_direction(self):
    self.a += (1.0-2.0*random())*self.angle_stp
    a = self.a
    self.dx = array([cos(a), sin(a)], 'float')*self.stp

  def _get_slope(self):
    size = self.size
    sand = self.sand
    xy = self.xy
    dx = self.dx
    fij = (((size*(xy+dx))+size)%size).astype('int')
    bij = (((size*(xy-dx))+size)%size).astype('int')
    slope = sand[fij[:,0],fij[:,1]] - sand[bij[:,0],bij[:,1]]
    return slope

  def _reselsect(self, stopping):
    size = self.size
    reselect_num = stopping.sum()
    count = 0
    # new_xy = random((reselect_num, 2))
    new_xy = zeros((reselect_num, 2), 'float')

    # TODO: vectors!!!!
    while count<reselect_num:
      nxy = random((1,2))
      ij = (size*nxy).astype('int')
      if self.sand[ij[0,0],ij[0,1]]>0:
        new_xy[count,:] = nxy
        count += 1

    nij = (size*new_xy).astype('int')
    self.xy[stopping,:] = new_xy
    self.sand[nij[:,0], nij[:,1]] -= 1

  def step(self):
    self.i += 1

    slope = self._get_slope()

    stopping = logical_or(slope<=0,random(slope.shape)>0.9)
    continuing = logical_not(stopping)

    ij = (self.xy[stopping,:]*self.size).astype('int')
    self.sand[ij[:,0],ij[:,1]] += 1

    self._reselsect(stopping)

    self.xy[continuing,:] = (self.xy[continuing,:]+self.dx)%1.0

    self._set_direction()
