import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
   (0., 0.),  # left, bottom
   (0., 10.),  # left, top
   (1., 1.),  # right, top
   (3., 6.),  # right, top
   (1., 0.),  # right, bottom
   (0., 0.),  # ignored
]

verts2 = [
   (0., 0.),  # left, bottom
   (0., 7.),  # left, top
   (6., 1.),  # right, top
   (6., 2.),  # right, top
   (4., 0.),  # right, bottom
   (0., 0.),  # ignored
]

codes = [
    Path.MOVETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.LINETO,
    Path.CLOSEPOLY,
]

path = Path(verts, codes)
path2 = Path(verts2, codes)

fig, ax = plt.subplots()
patch = patches.PathPatch(path, facecolor='orange', lw=1,alpha=.5)
patch2 = patches.PathPatch(path2, facecolor='green', lw=1,alpha=.5)
ax.add_patch(patch)
ax.add_patch(patch2)
ax.set_xlim(-2, 10)
ax.set_ylim(-2, 10)
plt.show()