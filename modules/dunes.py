# -*- coding: utf-8 -*-

from numpy import pi
from numpy.random import random
from numpy.random import randint
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
    delta = self.delta

    p = 0
    h = height[p]

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

  def _pick(self, x, y):
    self.sand[x,y] -=1
    self._shadow_row(x)

  def _deposit(self, x, y):
    self.sand[x,y] +=1
    self._shadow_row(x)

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
      x,y = randint(size, size=2)
      if sand[x,y]<1:
        continue
      if shadow[x,y]:
        continue
      return x,y

  def steps(self, steps=1000):
    size = self.size
    shadow = self.shadow

    for _ in range(steps):
      self.i += 1
      x,y = self._random_select()

      self._pick(x, y)
      while True:
        y = (y+1)%size
        if shadow[x,y] or random()<0.5:
          self._deposit(x,y)
          break

