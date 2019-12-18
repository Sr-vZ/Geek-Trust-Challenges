import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
matrix = np.array([[2, 2], [2, 2]])
xpos, ypos = np.meshgrid(
    np.arange(matrix.shape[0]), np.arange(matrix.shape[1]))
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)
dx = np.ones_like(zpos)
dy = dx.copy()
dz = matrix.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='y', zsort='average', linewidth=0)

l = max(matrix.shape[0], matrix.shape[1], matrix.max())
bb = np.array([(0, 0, 0), (0, l, 0), (l, 0, 0), (l, l, 0),
               (0, 0, l), (0, l, l), (l, 0, l), (l, l, l)])
ax.plot(bb[:, 0], bb[:, 1], bb[:, 2], "w", alpha=0.0)
ax.set_axis_off()
plt.show()
