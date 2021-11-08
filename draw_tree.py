import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import pandas as pd
import numpy as np


tree =  pd.read_csv('trees.csv', usecols=[1, 2, 3])
tree = np.array(tree)
plt.style.use('ggplot')
fig = plt.figure()
ax = p3.Axes3D(fig)
ax.plot(tree[:, 0], tree[:, 1], tree[:, 2], color='r')
plt.show()
