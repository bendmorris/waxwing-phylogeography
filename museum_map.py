import csv
import sys
from get_location import get_lat_lon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pkl
try: no_hits = pkl.load(open('no_hits.pkl'))
except: no_hits = set()


m = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=-50,resolution='i')
m.drawmapboundary(linewidth=0.25)
m.drawcoastlines(color='#6D5F47', linewidth=.1)
m.drawcountries(color='#6D5F47', linewidth=.1)

points = []
colors = ['red','blue']
species = {}
with open('museum_samples.csv') as input_file:
    reader = csv.reader(input_file)
    next(reader)
    for line in reader:
        sp = ' '.join(line[4].split()[:2])
        if not sp: continue
        lat, lon = line[8:10]
        country, state, county = line[13:16]
        locality = line[18]
        location_name = ', '.join([n for n in 
            (locality, county, state, country) if n])
        location_name = location_name.strip()
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
        x, y = m(lon, lat)
        if not sp in species:
            print ', '.join(species.keys()), sp
            species[sp] = colors.pop(0)
            
        points.append((x, y, species[sp]))


print len(points)
xs, ys, zs = [[point[n] for point in points] for n in range(len(points[0]))]
m.scatter(xs, ys, color=zs, s=5, marker='+')
plt.show()
