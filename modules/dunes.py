# -*- coding: utf-8 -*-

from numpy import pi
from numpy.random import random
from numpy import cos
from numpy import sin
from numpy import array
from numpy import zeros
from numpy import ones

from numpy import logical_not
from numpy import logical_or
from numpy import abs
from numpy import reshape
from numpy.linalg import norm

TWOPI = pi*2.0


class Dunes(object):

  def __init__(
      self,
      initial
      ):
    size, tmp = initial.shape
    if not size==tmp:
      raise ValueError('initial must be square')

    self.size = size
    self.one = 1.0/size
    self.delta = 4
    self.i = 0

    self.stp = self.one
    self.sand = zeros((size,size), 'int')
    self.sand[:,:] = initial
    self.shadow = zeros((size,size), 'bool')

    self._init_shadow_map()

  def _init_shadow_map(self):
    size = self.size
    sand = self.sand
    shadow = self.shadow
    delta = self.delta

    for i, height in enumerate(sand):
      p = 0
      h = height[p]
      # if i>10:
      #   break

      while True:
        long_shadow = True
        for d in range(1,delta+1):
          pd = p+d
          hd = height[pd]
          if hd>=h:
            h = hd
            long_shadow = False
            # print(i,p,h,hd,'break')
            break
          shadow[i, pd] = True

        p = pd
        if long_shadow:
          h = h-1 if h-1>0 else 0
        if p>=size-delta:
          break

  def get_normalized_sand(self):
    sand = self.sand.astype('float')
    flat = sand.reshape((-1,1))

    mi = flat.min()
    ma = flat.max()
    print(mi, ma)
    return (sand-mi)/(ma-mi)

  def get_shadow(self):
    return self.shadow.astype('float')

  # def _get_slope(self):
  #   size = self.size
  #   sand = self.sand
  #   xy = self.xy
  #   dx = self.dx
  #   fij = (((size*(xy+dx))+size)%size).astype('int')
  #   bij = (((size*(xy-dx))+size)%size).astype('int')
  #   slope = sand[fij[:,0],fij[:,1]] - sand[bij[:,0],bij[:,1]]
  #   return slope.astype('float')

  # def _reselsect(self, stopping):
  #   size = self.size
  #   reselect_num = stopping.sum()
  #   new_xy = zeros((reselect_num, 2), 'float')
  #
  #   # TODO: vectors!!!!
  #   count = 0
  #   while count<reselect_num:
  #     nxy = random((1,2))
  #     ij = (size*nxy).astype('int')
  #     if self.sand[ij[0,0],ij[0,1]]>0:
  #       new_xy[count,:] = nxy
  #       count += 1
  #
  #   nij = (size*new_xy).astype('int')
  #   self.xy[stopping,:] = new_xy
  #   self.sand[nij[:,0], nij[:,1]] -= 1

  def step(self):
    # slope = self._get_slope()
    # # stopping = logical_or(slope>=0,random(slope.shape)>0.95)
    # stopping = slope>0
    # continuing = logical_not(stopping)
    #
    # ijs = (self.xy[stopping,:]*self.size).astype('int')
    # self.sand[ijs[:,0],ijs[:,1]] += 1
    #
    # self._reselsect(stopping)
    #
    # # hh = (1.0+reshape(abs(slope[continuing]),
    # #     (continuing.sum(),1)))*self.dx/10.0
    #
    # ijc = (self.xy[continuing,:]*self.size).astype('int')
    # hh = self.sand[ijc[:,0], ijc[:,1]].astype('float')
    # hh = reshape(hh, (len(hh),1))/10.0*self.dx*random((len(hh), 1))
    # # print(norm(hh))
    # self.xy[continuing,:] = (self.xy[continuing,:]+hh)%1.0
    #
    # self._set_direction()
    self.i += 1
