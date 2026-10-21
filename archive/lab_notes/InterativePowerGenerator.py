import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pvlib
import matplotlib.dates as mdates
from matplotlib.widgets import Slider
import os
print(os.getcwd())  # Prints the current working directory


# Function to generate solar data
def create_data(year, month, latitude, longitude, tilt, orientation, capacity, shrinkage_factor):
    df = pd.DataFrame()

    # Define location (latitude, longitude, timezone, and altitude)
    location = pvlib.location.Location(latitude=latitude, longitude=longitude, tz='Etc/GMT+7')

    # Create timestamp column, every half-hour
    times = pd.date_range(start=f'{year}-{month}-01 00:00:00', periods=48*365, freq='30min', tz=location.tz)
    df['timestamp_utc'] = times

    # Calculate solar position
    solar_position = location.get_solarposition(times)

    # Calculate clear-sky irradiance
    clearsky_irradiance = location.get_clearsky(times)

    # Calculate total irradiance on a tilted surface
    irradiance = pvlib.irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=orientation,
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        dni=clearsky_irradiance['dni'],
        ghi=clearsky_irradiance['ghi'],
        dhi=clearsky_irradiance['dhi']
    )
    df['irradiance'] = irradiance['poa_global'].reindex(df['timestamp_utc']).values * capacity * shrinkage_factor
    return df

# Initial parameters
initial_latitude = 53.5
initial_longitude = -2.7
initial_tilt = 33
initial_orientation = 200
initial_capacity = 3.18
initial_shrinkage_factor = 0.0005

# Generate initial data
new_train_data_1 = create_data(2019, 3, 53.5, -2.7, initial_tilt, initial_orientation, initial_capacity, initial_shrinkage_factor)
new_train_data_1['timestamp_utc'] = pd.to_datetime(new_train_data_1['timestamp_utc'])

# Sample true data (Replace with actual data)
site_1_data = pd.read_csv('data/analytic_site_1_data.csv')
site_1_data['timestamp_utc'] = pd.to_datetime(site_1_data['timestamp_utc'])

# Create figure and axes
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, bottom=0.5)

# Plot initial data
(line1,) = ax.plot(new_train_data_1['timestamp_utc'], new_train_data_1['irradiance'], label='Analytic Data', alpha=0.5)
(line2,) = ax.plot(site_1_data['timestamp_utc'], site_1_data['solar_gen_kwh'], label='True Data', alpha=0.7)

# Set date formatting
locator = mdates.MonthLocator(bymonthday=1)
formatter = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.xticks(rotation=45)
plt.xlabel('Timestamp UTC')
plt.ylabel('Power Generation')
plt.legend()

# Create sliders for interactive control
ax_latitude = plt.axes([0.1, 0.3, 0.65, 0.03])
ax_longitude = plt.axes([0.1, 0.25, 0.65, 0.03])
ax_tilt = plt.axes([0.1, 0.2, 0.65, 0.03])
ax_orientation = plt.axes([0.1, 0.15, 0.65, 0.03])
ax_capacity = plt.axes([0.1, 0.1, 0.65, 0.03])
ax_shrinkage = plt.axes([0.1, 0.05, 0.65, 0.03])

slider_latitude = Slider(ax_latitude, "Latitude", 48, 61, valinit=initial_latitude)
slider_longitude = Slider(ax_longitude, "Longitude", -9, 2, valinit=initial_longitude)
slider_tilt = Slider(ax_tilt, "Tilt", 0, 90, valinit=initial_tilt)
slider_orientation = Slider(ax_orientation, "Orientation", 0, 360, valinit=initial_orientation)
slider_capacity = Slider(ax_capacity, "Capacity", 0.1, 10, valinit=initial_capacity)
slider_shrinkage = Slider(ax_shrinkage, "Shrinkage", 0.0001, 0.001, valinit=initial_shrinkage_factor)

# Function to update the plot when sliders change
def update(val):
    # Get new slider values
    new_latitude = slider_latitude.val
    new_longitude = slider_longitude.val
    new_tilt = slider_tilt.val
    new_orientation = slider_orientation.val
    new_capacity = slider_capacity.val
    new_shrinkage = slider_shrinkage.val

    # Generate updated data
    updated_data = create_data(2019, 3, new_latitude, new_longitude, new_tilt, new_orientation, new_capacity, new_shrinkage)
    updated_data['timestamp_utc'] = pd.to_datetime(updated_data['timestamp_utc'])

    # Update the plot
    line1.set_ydata(updated_data['irradiance'])
    fig.canvas.draw_idle()

# Connect sliders to update function
slider_latitude.on_changed(update)
slider_longitude.on_changed(update)
slider_tilt.on_changed(update)
slider_orientation.on_changed(update)
slider_capacity.on_changed(update)
slider_shrinkage.on_changed(update)

plt.show()
