# -*- coding: utf-8 -*-

from numpy import pi
from numpy.random import random
from numpy.random import randint
from numpy.random import shuffle
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
    for i in range(self.size):
      self._shadow_row(i)

  def _shadow_row(self, i):
    height = self.sand[i, :]
    size = self.size
    shadow = self.shadow
    shadow[i,:] = False
    delta = self.delta

    p = 0
    h = height[p]

    while True:
      # TODO: handle continuous boundary
      long_shadow = True
      for d in range(1,delta+1):
        pd = p+d
        hd = height[pd]
        if hd>=h:
          h = hd
          long_shadow = False
          break
        shadow[i, pd] = True

      p = pd
      if long_shadow:
        h = h-1 if h-1>0 else 0
      if p>=size-delta:
        break

  def _cascade(self, i, j):
    height = self.sand[i,j]
    sand = self.sand
    size = self.size
    order = [0,1,2,3]
    shuffle(order)
    directions = (array([
      [i,j-1],
      [i,j+1],
      [i-1,j],
      [i+1,j],
      ], 'int')%size)[order,:]

    for d in directions:
      df = height-sand[d[0], d[1]]
      if abs(df)>2:
        if df<0:
          sand[d[0],d[1]]-=1
          sand[i,j] += 1
        else:
          sand[d[0],d[1]]+=1
          sand[i,j] -= 1
        return d[1]
    return None

  def _erode(self, i, j, additive=False):
    if additive:
      self.sand[i,j] +=1
    else:
      self.sand[i,j] -=1

    r = self._cascade(i, j)
    if r is not None and r is not i:
      self._shadow_row(r)
    self._shadow_row(i)

  def get_normalized_sand(self):
    sand = self.sand.astype('float')
    flat = sand.reshape((-1,1))

    mi = flat.min()
    ma = flat.max()
    print(mi, ma)
    return (sand-mi)/(ma-mi)

  def get_shadow(self):
    return self.shadow.astype('float')

  def _random_select(self):
    size = self.size
    sand = self.sand
    shadow = self.shadow
    while True:
      i,j = randint(size, size=2)
      if sand[i,j]<1:
        continue
      if shadow[i,j]:
        continue
      return i,j

  def steps(self, steps=1000):
    size = self.size
    shadow = self.shadow

    for _ in range(steps):
      self.i += 1
      i,j = self._random_select()

      self._erode(i, j, additive=False)
      while True:
        j = (j+1)%size
        if shadow[i,j] or random()<0.24:
          self._erode(i,j,additive=True)
          break

