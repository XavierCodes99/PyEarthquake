import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pyaudio
import wave

from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from datetime import datetime

# Define the colormap
colormap = ListedColormap(['#0ff', '#00f', '#0f0', '#af0', '#ff0', '#fa0', '#f00', '#a00', '#e0f'])

# Initialize the plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)

m = Basemap(projection='merc', llcrnrlon=-180, llcrnrlat=-80, urcrnrlon=180, urcrnrlat=80, resolution='l')

m.drawmapboundary(fill_color='#aff')  # Color for the oceans
m.fillcontinents(color='#afa', lake_color='#cff', zorder=1)  # Colors for the land and lakes

m.drawcoastlines()
m.drawcountries()

# Initialize the scatter plot
sc = ax.scatter([], [], [], alpha=0.75, cmap=colormap, edgecolor='black', zorder=2, marker="o")

# Add a colorbar
cbar = plt.colorbar(sc, label='Magnitude')

# Set the x and y limits
ax.set_xlim(m.llcrnrx, m.urcrnrx)
ax.set_ylim(m.llcrnry, m.urcrnry)

# Text annotation properties
annotation_kwargs = dict(facecolor='white', alpha=0.75, edgecolor='black', boxstyle='round,pad=0.3')
earthquake_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, ha='left', va='top', fontsize=10, bbox=annotation_kwargs)

# Function to convert time to 12-hour format
def convert_to_12_hour_format(time_str):
    time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time_obj.strftime("%Y-%m-%d %I:%M:%S %p")

# Initialize a variable to keep track of the warning text
warning_displayed = False

def play_sound():
    filename = 'sounds/Warning.wav'  # Replace with the path to your sound file
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

# Update the plot with new data
def update_plot(i):
    global warning_displayed
    
    # Read the CSV file
    df = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv')

    # Extract the columns
    lat = df['latitude']
    lon = df['longitude']
    mag = df['mag']
    place = df['place']
    time = df['time']

    x, y = m(lon, lat)

    # Normalize the color values
    max_mag = mag.max()
    colors = max_mag / mag

    # Update the scatter plot
    sc.set_offsets(list(zip(x, y)))
    sc.set_array(mag)
    sc.set_cmap(colormap)
    sc.set_sizes(np.exp(mag))
    sc.set_clim(vmin=1, vmax=9)

    # Annotate the plot with earthquake information
    if len(df) > 0 and not warning_displayed:
        eq_info = f"Earthquake occurred at:\n{place.iloc[0]}\nTime: {convert_to_12_hour_format(time.iloc[0])}"
        earthquake_text.set_text(eq_info)

        # Clear the warning text after 5 seconds (5000 milliseconds)
        warning_displayed = True  # Set the flag to True
        ani.event_source.stop()
        plt.pause(10)  # Pause for 5 seconds
        earthquake_text.set_text('')
        ani.event_source.start()

    fig.canvas.manager.set_window_title('PyEarthquake')

# Animate the plot
ani = FuncAnimation(fig, update_plot, interval=1000)

plt.show()
