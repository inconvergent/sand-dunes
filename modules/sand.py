  #!/usr/bin/python
# -*- coding: utf-8 -*-

from numpy import pi
from numpy.random import random
from numpy import zeros
from numpy import arange
from numpy import cos
from numpy import sin
from numpy import round


TWOPI = pi*2.0


class Sand(object):

  def __init__(self, size, angle_stp=0.5):

    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp
    self.a = random()*TWOPI
    self.i = 0

    self.s = random(size=(self.size2))
    self.inds = arange(self.size2)
    self.inds_2d = self.inds.reshape((size,-1))
    # self.inds = np.arange(size*size).reshape((size,-1))


  def __wind(self):

    size2 = self.size2
    size = self.size

    a = self.a + (1.0-2*random(size=(size2)))*0.1
    i = round(cos(a))
    j = round(sin(a))
    ij = (i*size+j).astype('int')

    upwind = self.inds + ij
    upwind[upwind<0] = 0
    upwind[upwind>size2-1] = size2-1
    s = self.s

    diff = (s[self.inds] - s[upwind])

    s[self.inds] += diff*0.2
    print()
    print('diff',diff.min(), diff.max())
    print('s',s.min(), s.max())

  def get_sand(self):

    return self.s

  def get_normalized_sand(self):

    s = self.s
    mi = s.min()
    ma = s.max()

    return (s-mi)/(ma-mi)

  def step(self):

    self.i += 1

    self.__wind()

    self.a += (1.0-2.0*random())*self.angle_stp
    # S = random(size=(size,size))

    return True

