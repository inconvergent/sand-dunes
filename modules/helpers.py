# -*- coding: utf-8 -*-

def get_colors(f, do_shuffle=True):
  from numpy import array
  try:
    import Image
  except Exception:
    from PIL import Image

  im = Image.open(f)
  data = array(list(im.convert('RGB').getdata()),'float')/255.0

  res = []
  for rgb in data:
    res.append(list(rgb))

  if do_shuffle:
    from numpy.random import shuffle
    shuffle(res)
  return res

def get_img_as_rgb_array(f):
  from PIL import Image
  from numpy import array
  from numpy import reshape
  im = Image.open(f)
  w,h = im.size
  data = array(list(im.convert('RGB').getdata()), 'float')/255.0
  return reshape(data,(w,h,3))

