# 
"""
Author: Yifei with aid from chatGPT
Date: 2024.Nov
Purpose: This script predicts the power generation of a solar panel based on the sun's angle and other parameters.
Functions:
    Power_predict(date, time, latitude, longitude, tile_angle, orientation_angle, power_capacity)
        Predicts the power generation of a solar panel.
        Parameters:
            date (str): The date for which to predict power generation.
            time (str): The time for which to predict power generation.
            latitude (float): The latitude of the solar panel's location.
            longitude (float): The longitude of the solar panel's location.
            tile_angle (float): The tilt angle of the solar panel.
            orientation_angle (float): The orientation angle of the solar panel.
            power_capacity (float): The power capacity of the solar panel in watts.
        Returns:
            float: The predicted power generation in kilowatt-hours (kWh).
"""
import math
from datetime import datetime
from SunAnglePredict import get_sun_angle
from PowerGeneration import calculate_power_generation


def Power_predict(date, time, latitude, longitude, tile_angle, orientation_angle, power_capacity):
    
    # Get the sun's angle using the provided date, time, latitude, and longitude
    angle_of_incidence = get_sun_angle(date, time, latitude, longitude)
    # Calculate power generation
    power_generation = calculate_power_generation(angle_of_incidence, power_capacity)
    # Convert power generation to kWh
    power_generation_kWh = power_generation / 1000
    
    return power_generation_kWh