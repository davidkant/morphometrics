import morphometrics.core

import matplotlib.pyplot as plt

def plot(self, ax=None):
  """Plot a morph."""

  if ax == None: ax = plt.subplot() # create axes if not given
  plt.title(str(self.x)) # title it
  plt.plot(self.x, c='black') # plot
  ax.xaxis.set_visible(False) # hide axis labels
  ax.yaxis.set_visible(False) # hide axis labels
  plt.xlim([-1, len(self.x)]) # padding
  plt.ylim([min(self.x)-1, max(self.x)+1]) # padding
  for edge_key in ax.spines: ax.spines[edge_key].set_color('grey') # grey border
  plt.scatter(range(len(self.x)), self.x, c='black') # show points

morphometrics.core.Morph.plot = plot