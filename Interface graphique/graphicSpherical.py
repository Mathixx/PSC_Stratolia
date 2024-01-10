import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def update(num):
    global balloon_trajectory

    x = balloon_trajectory[:, 0]
    y = balloon_trajectory[:, 1]

    plt.cla()
    line, = ax.plot(x[:num+1], y[:num+1], marker='o', linestyle='-', transform=ccrs.PlateCarree())
    
    return [line]

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_extent([-75.0, -70.0, 35.0, 40.0])

ax.add_feature(cfeature.LAND, facecolor='gray')
ax.add_feature(cfeature.OCEAN, facecolor='w')
ax.add_feature(cfeature.STATES, linestyle=':')
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.COASTLINE, linestyle=':')

balloon_trajectory = np.random.rand(100, 2)

ani = FuncAnimation(fig, update, frames=range(len(balloon_trajectory)), interval=50, blit=True)

plt.show()