import numpy as np
import math
import matplotlib.pyplot as plt

#--------------------------------------------------------------------------------------------------#
# BASIS
#--------------------------------------------------------------------------------------------------#

# basis L3
b1 = np.array([1,  0, -1])
b2 = np.array([0,  1,  1]) 
basis_L3 = [b1, b2]

# basis L4
b1 = np.array([1, 0, 0, -1, -1,  0])
b2 = np.array([0, 1, 0,  1,  0, -1])
b3 = np.array([0, 0, 1,  0,  1,  1])
basis_L4 = [b1,b2,b3]

# basis L5
b1 = np.array([1, 0, 0, 0, -1, -1, -1,  0,  0,  0])
b2 = np.array([0, 1, 0, 0,  1,  0,  0, -1, -1,  0])
b3 = np.array([0, 0, 1, 0,  0,  1,  0,  1,  0, -1])
b4 = np.array([0, 0, 0, 1,  0,  0,  1,  0,  1,  1])
basis_L5 = [b1,b2,b3,b4]

def contour_length_to_L(x):
  """contour length to L"""

  # FUCKING: i think we just need the + solution...

  a,b,c = 1,-1,-2*x

  return int((-1*b + math.sqrt(b**2 - 4*a*c)) / 2*a)

def basis_rank_to_L(x):
  """basis rank to L"""

  return x + 1

def L_to_contour_length(L): 
  """L to contour length"""

  return (L**2 - L) / 2

def L_to_basis_rank(L):
  """L to basis rank"""

  return L - 1

def L_to_basis(L):
  """return basis for morph length L"""

  if L==3: return basis_L3
  if L==4: return basis_L4
  if L==5: return basis_L5
  else: print('nope')

#--------------------------------------------------------------------------------------------------#
# COORDINATE SYSTEMS [API]
#--------------------------------------------------------------------------------------------------#

class Mobject:

  def __init__(self, x):
    self.x = x

  def __getitem__(self, index):
    return self.x[index]

class Morph(Mobject):
    
  # def as_contour(self):
    # return Contour(differentiate(self.x))

  # def as_basis(self):
    # return self.as_contour().as_basis()

  def L(self):
    return len(self.x)

  def __repr__(self):
    return 'Morph{0}'.format(self.x)

class Contour(Mobject):

  def as_morph(self):
    return Morph(integrate(self.as_contour()))
 
  def as_contour(self):
    return self

  def as_basis(self):
    
    # basis
    basis = L_to_basis(self.L())

    return Basis(change_of_basis(self.x), basis)

  def L(self):
    return contour_length_to_L(len(self.x))
    
  def __eq__(self, other):
    return self.x == other.as_contour().x

  def __repr__(self):
    return 'Contour{0}'.format(self.x)

class Basis(Mobject):

  def as_morph(self):
    return Morph(integrate(self.as_contour()))

  def as_contour(self):
     
    # basis
    basis = L_to_basis(self.L())

    return Contour(a_times_x(basis, self.x))

  def as_basis(self):
    return self

  def L(self):
    return basis_rank_to_L(len(self.x))

  def __eq__(self, other):
    return self.x == other.as_basis().x

  def __repr__(self):
    return 'Basis{0}'.format(self.x)

#--------------------------------------------------------------------------------------------------#
# CONVERTERS [INTERNALS]
#--------------------------------------------------------------------------------------------------#

def change_of_basis(coords, basis):
  """(contour space to basis space)"""
  
  # matrices
  a = np.matrix(np.vstack(basis)).getT()
  b = np.matrix(coords).getT()
  
  # solve
  soln = a.getI() * b
  
  # return as list
  return np.array(soln)[:,0].tolist()

def a_times_x(a, x):
  """(basis space to contour space)"""

  # matrices
  a = np.matrix(np.vstack(a)).getT()
  x = np.matrix(np.vstack(x))

  # multiply
  soln = a * x

  # return as list
  return np.array(soln)[:,0].tolist()

def clip(xs):

  return map(lambda x: 1 if x>0 else -1 if x<0 else 0, xs)

def integrate(xs):
  """(contour space to morph space) integrates along half matrix diagonal"""
  
  # initial value
  initial_value = 0

  # take (half matrix) diagonal
  indices = np.concatenate((np.array([0]),np.cumsum(np.arange(m.L())[::-1][:-2])))
  diagonal = np.array(xs)[indices]

  # integrate
  morph = [initial_value] + np.cumsum(diagonal).tolist()
    
  # normal form
  # morph = Morph(morph).to_normal()
    
  return morph

# def differentiate(xs):


#--------------------------------------------------------------------------------------------------#
# NORMAL FORMS
#--------------------------------------------------------------------------------------------------#

def is_morph_normal(self):
  """Is the morph in normal form?

  a morph is in normal form iff:
      [1] zeroed: min elem is 0
      [2] compact: num of unique elements = max - min (+1)
  """
  unique = tuple(set(self.morph))
  return min(self.morph) == 0 and (max(unique) - min(unique) + 1) == len(unique)

def to_morph_normal(self):
  """Convert a morph to normal form.

  conversion to normal form:
      [1] zero: move minimum elem to 0
      [2] compact: compresse so num of unique elements = max - min (+1)
  """
  zeroed = [elem - min(self.morph) for elem in self.morph]
  unique = tuple(sorted(set(zeroed)))               
  return Morph(tuple(unique.index(e) for e in zeroed))

def is_basis_normal(c):
  """Is the contour in basis normal form?

    a basis is in normal form iff:
      [1] abs(elems) <= len(c)
      [2] stellation form:
            
            for n != [-1,0,1]: (all combinations of +/- 1s and 0s are OK)
              if n (positive) then n-1
              if n (negative) then n+1
  """
  one = abs(max(c)) <= len(c)

  def mlessone(x):
    if x > 0: return x - 1
    if x < 0: return x + 1
    else: return 0

  two = all([mlessone(elem) in c for elem in filter(lambda x: abs(x)>1, c)])

  return one and two
























