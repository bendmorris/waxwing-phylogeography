from get_location import get_lat_lon


with open('sample_locations') as input_file:
    for line in input_file:
        line = line.strip()
        values = line.split(':')
        id, location, short_location = values[:3]
        if len(values) > 3:
            other = ':'.join(values[3:])
            latlon = None
        else: 
            other = None
            latlon = get_lat_lon(location)

        if not other and latlon:
            lat1, lon1, lat2, lon2 = latlon
            lat = round((lat1+lat2)/2, 2)
            lon = round((lon1+lon2)/2, 2)
            print ':'.join((id, location, short_location, str(lat), str(lon)))
        else:
            print ':'.join((id, location, short_location) + ((other,) if other else ()))