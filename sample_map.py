from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys
import random


if len(sys.argv) > 1:
    filename = sys.argv[1]
else: filename = None

colors = {'Bombycilla garrulus': 'Blue',
          'Bombycilla cedrorum': 'Red',
          None: 'Yellow'}
samples = {}
with open('bombycillidae.fasta') as input_file:
    for line in input_file:
        if line[0] == '>':
            parts = line[1:].strip().split('.')
            sample_name = '.'.join(parts[:2])
            species_name = ' '.join(parts[2:])
            samples[sample_name] = species_name
            
all_species = sorted(list(set(samples.values())))

plt.figure(dpi=500)

m = Basemap(projection='cyl',llcrnrlat=30,urcrnrlat=90,
            llcrnrlon=-180,urcrnrlon=180,resolution='i')
m.drawmapboundary(linewidth=0.25)
m.drawcoastlines(color='#6D5F47', linewidth=.1)
m.drawcountries(color='#6D5F47', linewidth=.1)
#m.drawmeridians(np.arange(-180, 180, 30), color='#bbbbbb')
#m.drawparallels(np.arange(-90, 90, 30), color='#bbbbbb')


xs, ys, zs = [], [], []
with open('filled_sample_locations') as input_file:
    for line in input_file:
        line = line.strip()
        if not line: continue
        try:
            sample, loc, shortloc, lat, lon = line.split(':')
            lat, lon = float(lat) + random.random()-0.5, float(lon) + random.random()-0.5
        except: continue
        x, y = m(lon, lat)
        xs.append(x); ys.append(y)
        try:
            z = colors[samples[sample]]
        except Exception as e: 
            z = colors[None]

        zs.append(z)

m.scatter(xs, ys, color=zs, s=5, marker='+')
if filename: plt.savefig(filename)
else: plt.show()
