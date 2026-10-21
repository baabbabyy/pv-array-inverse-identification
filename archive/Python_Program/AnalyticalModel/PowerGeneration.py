import math


def calculate_power_generation(sun_angle, panel_tilt, panel_orientation, power_capacity):
    # Calculate the angle of incidence
    angle_of_incidence = math.radians(sun_angle - panel_tilt - panel_orientation)
    
    # Calculate the power generation
    power_generation = power_capacity * max(0, math.cos(angle_of_incidence))
    
    return power_generation
