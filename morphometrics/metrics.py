#--------------------------------------------------------------------------------------------------#
# METRICS 
#--------------------------------------------------------------------------------------------------#

def OCM_hat(m1, m2):

  return sum([abs(x-y) for x,y in zip(m1.as_contour().x, m2.as_contour().x)])

def OCM(m1, m2):

  return sum([abs(x-y) for x,y in zip(m1.as_contour().x, m2.as_contour().x)])

def OCD(m1, m2):

  return sum([min(1,abs(x-y)) for x,y in zip(m1.as_dcontour().x, m2.as_dcontour().x)])

