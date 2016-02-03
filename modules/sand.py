# -*- coding: utf-8 -*-

from __future__ import print_function

from numpy import pi
from numpy.random import random
from numpy import arange
from numpy import cos
from numpy import sin
from numpy import round
from numpy import zeros


TWOPI = pi*2.0



class Sand(object):

  def __init__(self, size, angle_stp=0.5):

    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp

    self.a = 0.3*TWOPI
    self.i = 1

    self.__init_inds()
    self.__init_frame()
    self.__init_s('line')

  def __init_inds(self):

    size = self.size
    size2 = self.size2
    self.inds = arange(size2)
    self.inds_2d = self.inds.reshape((size,-1))

  def __init_frame(self):

    size = self.size
    size2 = self.size2
    frame = zeros((size,size), 'float')
    frame[0,:] = 1.
    frame[size-1,:] = 1.
    frame[:,size-1] = 1.
    frame[:,0] = 1.
    self.frame = frame.astype('bool').reshape((size2,-1)).flatten()

  def __init_s(self, t='random'):

    size = self.size
    size2 = self.size2

    if t == 'random':
      self.s = random(size=self.size2)
    elif t == 'img':
      from utils import get_dens_from_img
      self.s = 1.0-get_dens_from_img('./img/x512.png').reshape((size2,-1)).flatten()
    elif t == 'line':
      self.s = zeros(self.size2, 'float').reshape((size,-1))
      self.s[int(size/2.0),:] = 1.0
      self.s = self.s.reshape((size2,-1)).flatten()

    sb = zeros(self.s.shape,'float')
    self.sb = sb
    self.sb[:] = self.s[:]


  def __wind(self):

    size2 = self.size2
    size = self.size
    inds = self.inds
    frame = self.frame
    s = self.s
    sb = self.sb

    # a = self.a + (1.0-2*random(size=size2))
    from numpy import ones
    a = self.a*ones(size2)

    i = round(cos(a))
    j = round(sin(a))

    i[frame] = 0.0
    j[frame] = 0.0


    ij = (i*size+j).astype('int')

    upwind = self.inds + ij
    # upwind[upwind<0] = 0
    # upwind[upwind>size2-1] = size2-1
    # diff = (s[upwind] - s[inds])*0.2

    # print(inds.reshape(size,-1))
    # print(ij.reshape(size,-1))
    # print(upwind.reshape(size,-1))

    # mask = random(size=size2)>s
    # diff[mask] = 0.

    sb = s[:]
    s[inds] -= sb[upwind]*0.1
    s[upwind] += sb[inds]*0.1

    # s[inds] -= diff
    # s[upwind] += diff
    # s[frame] = 0.0

  def get_sand(self):

    return self.s

  def get_normalized_sand(self, dbg=False):

    s = self.s
    mi = s.min()
    ma = s.max()

    res = (s-mi)/(ma-mi)
    if dbg:
      print('s', mi, ma)
      # print(res.reshape((self.size,-1)))

    return res

  def step(self):

    self.i += 1

    self.__wind()

    self.a += (1.0-2.0*random())*self.angle_stp
    # print('a', self.a)

    return True

