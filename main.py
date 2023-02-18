import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

# Define the colormap
colormap = ListedColormap(['#ccc', '#0ff', '#00f', '#0f0', '#af0', '#ff0', '#fa0', '#f00', '#a00', '#a0f'])

# Initialize the plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

m = Basemap(projection='merc', llcrnrlon=-180, llcrnrlat=-80, urcrnrlon=180, urcrnrlat=80, resolution='l')

m.drawcoastlines()
m.drawcountries()

# Initialize the scatter plot
sc = ax.scatter([], [], [], alpha=0.75, cmap=colormap, edgecolor='black', zorder=2, marker="*")

# Add a colorbar
cbar = plt.colorbar(sc, label='Magnitude')

# Set the x and y limits
ax.set_xlim(m.llcrnrx, m.urcrnrx)
ax.set_ylim(m.llcrnry, m.urcrnry)

# Update the plot with new data
def update_plot(i):
    # Read the CSV file
    df = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv')

    # Extract the columns
    lat = df['latitude']
    lon = df['longitude']
    mag = df['mag']

    x, y = m(lon, lat)
    
    # Normalize the color values
    max_mag = mag.max()
    colors = max_mag / mag

    # Update the scatter plot
    sc.set_offsets(list(zip(x, y)))
    sc.set_array(mag)
    sc.set_cmap(colormap)
    sc.set_sizes(np.exp(mag) // 5)
    sc.set_clim(vmin=0, vmax=10)
    
    fig.canvas.manager.set_window_title('PyQuake')

# Animate the plot
ani = FuncAnimation(fig, update_plot, interval=1000)

plt.show()