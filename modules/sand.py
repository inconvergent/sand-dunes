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

def get_dens_from_img(fn):

  from scipy.ndimage import imread

  return imread(fn)/255.


class Sand(object):

  def __init__(self, size, angle_stp=0.5):

    self.size = size
    self.size2 = size*size
    self.one = 1.0/size
    self.angle_stp = angle_stp
    self.a = random()*TWOPI
    self.i = 0

    self.s = random(size=(self.size2))
    # self.s = get_dens_from_img('./img/x512.png').reshape((self.size2,-1)).flatten()

    self.inds = arange(self.size2)
    self.inds_2d = self.inds.reshape((size,-1))
    # self.inds = np.arange(size*size).reshape((size,-1))


  def __wind(self):

    size2 = self.size2
    size = self.size
    inds = self.inds
    s = self.s

    a = self.a + (1.0-2*random(size=size2))*0.1
    rad = self.s*random(size=size2)*10.0
    i = round(cos(a)*rad)
    j = round(sin(a)*rad)
    ij = (i*size+j).astype('int')

    upwind = self.inds + ij
    upwind[upwind<0] = 0
    upwind[upwind>size2-1] = size2-1

    diff = (s[inds] - s[upwind])*0.2
    s[inds] -= diff
    s[upwind] += diff


  def get_sand(self):

    return self.s

  def get_normalized_sand(self, dbg=False):

    s = self.s
    mi = s.min()
    ma = s.max()

    if dbg:
      print('s', mi, ma)

    return (s-mi)/(ma-mi)

  def step(self):

    self.i += 1

    self.__wind()

    self.a += (1.0-2.0*random())*self.angle_stp
    print('a', self.a)
    # S = random(size=(size,size))

    return True

