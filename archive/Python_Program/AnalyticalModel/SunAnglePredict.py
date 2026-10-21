import datetime
    def get_sun_angle(location, date, time):
        latitude, longitude = location
        dt = datetime.datetime.combine(date, time)
        day_of_year = dt.timetuple().tm_yday

        declination_angle = calculate_declination_angle(day_of_year)
        hour_angle = calculate_hour_angle(dt, longitude)
        solar_elevation_angle = calculate_solar_elevation_angle(latitude, declination_angle, hour_angle)
        solar_azimuth_angle = calculate_solar_azimuth_angle(hour_angle, latitude, declination_angle, solar_elevation_angle)
        angle_of_incidence = calculate_angle_of_incidence(solar_elevation_angle, tile_angle, solar_azimuth_angle, orientation_angle)

        return {
            "declination_angle": declination_angle,
            "hour_angle": hour_angle,
            "solar_elevation_angle": solar_elevation_angle,
            "solar_azimuth_angle": solar_azimuth_angle,
            "angle_of_incidence": angle_of_incidence
        }
    