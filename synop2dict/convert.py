from pymetdecoder import synop as s
import math


# Enumerate the keys
keys = ['station_type', 'year', 'month', 'day', 'hour', 'minute',
        'wind_indicator', 'station_id', 'region',
        'precipitation_indicator', 'weather_indicator',
        'lowest_cloud_base', 'visibility', 'cloud_cover',
        'wind_direction', 'wind_speed', 'air_temperature',
        'dewpoint_temperature', 'station_pressure', 'sea_level_pressure',
        '3_hour_pressure_change', 'precipitation_s1', 'present_weather',
        'past_weather', 'low_cloud_type', 'low_cloud_amount',
        'middle_cloud_type', 'high_cloud_type']

# Build the dictionary template
synop_template = dict.fromkeys(keys)


def convert_to_dict(message, year, month):
    """This function uses Pymetdecoder to convert the SYNOP message, then strips values
        from this and converts units to output a dictionary ready to be
        converted to BUFR.

        Args:
            message (str): The message to be decoded.
            year (int): The assigned year of the message.
            month (int): The assigned month of the message.
    """

    # Get the full output decoded message from the Pymetdecoder package
    decode = s.SYNOP().decode(message)

    # Get the template dictionary to be filled
    output = synop_template

    # !Convert and assign to the template dictionary

    # *The following do not need to be converted

    output['station_type'] = message[0:5]
    output['year'] = year
    output['month'] = month

    if 'obs_time' in decode.keys():
        output['day'] = decode['obs_time']['day']['value']
        output['hour'] = decode['obs_time']['hour']['value']

    # *The minute will be 00 unless specified by exact observation time
    if 'exact_obs_time' in decode.keys():
        output['minute'] = decode['exact_obs_time']['minute']['value']
    else:
        output['minute'] = 0

    if 'wind_indicator' in decode.keys():
        output['wind_indicator'] = decode['wind_indicator']['value']

    if 'station_id' in decode.keys():
        output['station_id'] = decode['station_id']['value']

    if 'region' in decode.keys():
        output['region'] = decode['region']['value']

    if 'precipitation_indicator' in decode.keys():
        output['precipitation_indicator'] = decode['precipitation_indicator']['value']

    if 'weather_indicator' in decode.keys():
        output['weather_indicator'] = decode['weather_indicator']['value']

    # *Lowest cloud base is already given in metres, but we specifically select the minimum value
    if 'lowest_cloud_base' in decode.keys():
        output['lowest_cloud_base'] = decode['lowest_cloud_base']['min']

    # *Visibility is already given in metres
    if 'visibility' in decode.keys():
        output['visibility'] = decode['visibility']['value']

    # *Cloud cover is given in oktas, which we convert to a percentage rounded up
    if 'cloud_cover' in decode.keys():
        N_oktas = decode['cloud_cover']['value']
        # If the cloud cover is 9 oktas, this means the sky was obscured and we keep the value as None
        if N_oktas < 9:
            N_percentage = math.ceil((N_oktas / 8) * 100)
            output['cloud_cover'] = N_percentage

    # *Wind direction is already in degrees
    if 'wind_direction' in decode.keys():
        output['wind_direction'] = decode['wind_direction']['value']

    # *Wind speed is given in the units specified by 'wind_indicator', which we use to convert to m/s
    if 'wind_speed' in decode.keys():
        ff = decode['wind_speed']['value']

        # Find the units
        ff_unit = decode['wind_indicator']['unit']

        # If units are knots instead of m/s, convert it to knots
        if ff_unit == 'KT':
            ff *= 0.5144

        output['wind_speed'] = ff

    # *All temperatures are given in celcius, which we convert to kelvin and then round to 2dp
    if 'air_temperature' in decode.keys():
        output['air_temperature'] = round(
            decode['air_temperature']['value'] + 273.15, 2)
    if 'dewpoint_temperature' in decode.keys():
        output['dewpoint_temperature'] = round(
            decode['dewpoint_temperature']['value'] + 273.15, 2)

    # *Pressure is given in hPa, which we convert to Pa
    if 'station_pressure' in decode.keys():
        output['station_pressure'] = decode['station_pressure']['value'] * 100
    if 'sea_level_pressure' in decode.keys():
        output['sea_level_pressure'] = decode['sea_level_pressure']['value'] * 100
    if 'pressure_tendency' in decode.keys():
        output['3_hour_pressure_change'] = decode['pressure_tendency']['change']['value'] * 100

    # *Precipitation is given in mm, which we convert to m
    if 'precipitation_s1' in decode.keys():
        output['precipitation_s1'] = decode['precipitation_s1']['amount'] * 0.001

    # *What to do here?
    if 'present_weather' in decode.keys():
        output['present_weather'] = decode['present_weather']['value']
    if 'past_weather' in decode.keys():
        output['past_weather_1'] = decode['past_weather'][0]['value']
        output['past_weather_2'] = decode['past_weather'][1]['value']

    # *Cloud types are untouched
    if 'cloud_types' in decode.keys():
        output['low_cloud_type'] = decode['cloud_types']['low_cloud_type']['value']
        output['middle_cloud_type'] = decode['cloud_types']['middle_cloud_type']['value']
        output['high_cloud_type'] = decode['cloud_types']['high_cloud_type']['value']

        # *Low cloud amount is given in oktas, which we convert to a rounded up percentage
        N_oktas = decode['cloud_types']['low_cloud_amount']['value']
        # If the cloud cover is 9 oktas, this means the sky was obscured and we keep the value as None
        if N_oktas < 9:
            N_percentage = math.ceil((N_oktas / 8) * 100)
            output['low_cloud_amount'] = N_percentage

    # !Return the new dictionary
    return output
