import csv
import sys
from get_location import get_lat_lon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pkl
try: no_hits = pkl.load(open('no_hits.pkl'))
except: no_hits = set()


MIN_SPECIMENS = 50

points = {}
colors = ['red', 'blue', 'green', 'yellow', 'orange']
species = {}
with open('museum_samples.csv') as input_file:
    reader = csv.reader(input_file)
    next(reader)
    for line in reader:
        prep = line[6].lower()
        if prep and (any([n in prep for n in ('whole','bird','body','mount')])): continue

        museum, collection = line[:2]
        if not collection == 'ORN': continue

        sp = ' '.join(line[4].split()[:2])
        if not sp: continue

        lat, lon = line[8:10]
        country, state, county = line[12:15]
        county = county.replace('Co.', 'County')
        locality = line[17]
        location_name = ', '.join([n for n in 
            (locality, county, state, country) if n])
        location_name = location_name.strip().replace('.', '')
        if not location_name: continue
        if location_name in no_hits: continue
        if not lat or not lon:
            print location_name,
            sys.stdout.flush()
            try: 
                lat1, lon1, lat2, lon2 = get_lat_lon(location_name)
                lat = (lat1+lat2)/2
                lon = (lon1+lon2)/2
            except Exception as e: 
                print e
                no_hits.add(location_name)
                pkl.dump(no_hits, open('no_hits.pkl', 'w'), -1)
                continue
            print lat, lon
        else:
            lat, lon = float(lat), float(lon)
            print location_name, lat, lon
        
        if not museum in points: points[museum] = []
        if not sp in species:
            species[sp] = colors.pop(0)
        color = species[sp]
        points[museum].append((lon, lat, color))


for key in points:
    if len(points[key]) < MIN_SPECIMENS: continue

    plt.figure()
    plt.title('%s (n=%s)' % (key, len(points[key])))

    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,
                llcrnrlon=-180,urcrnrlon=180,resolution='l')
    m.drawmapboundary(linewidth=0.25)
    m.drawcoastlines(color='#6D5F47', linewidth=.1)
    m.drawcountries(color='#6D5F47', linewidth=.1)

    print key, len(points[key])
    xs, ys, zs = [[point[n] for point in points[key]] for n in range(len(points[key][0]))]
    m.scatter(xs, ys, color=zs, s=5, marker='+')

    plt.savefig('museums/%s.png' % key)

plt.show()
