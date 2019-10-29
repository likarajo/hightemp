import datetime
import pandas as pd
import numpy as np
#%matplotlib  #(in iPython)
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

now = datetime.datetime.now()
#DATA_URL = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_Global_24h.csv"
DATA_URL = "https://firms.modaps.eosdis.nasa.gov/active_fire/c6/text/MODIS_C6_USA_contiguous_and_Hawaii_24h.csv"
data = pd.read_csv(DATA_URL)
print("Data fetched at " + now.strftime("%Y-%m-%d %H:%M"))

data = data[data['confidence']>50] # filter the data to only have higher confidence once
data = data[data['brightness']>400] # filter the data to only have higher temperature that are a fire hazard
df = data[['latitude','longitude','brightness','frp']] # extract only important attributes

fig, ax = plt.subplots(figsize=(8, 8))

parallels=np.arange(-80,81,1.)
meridians = np.arange(10.,351.,1.)

m = Basemap(ax=ax, epsg=4326, resolution='h',
    llcrnrlon=-125. ,llcrnrlat=32., urcrnrlon=-114. ,urcrnrlat=43.)

m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS',
    service='ESRI_Imagery_World_2D',
    xpixels=400, ypixels=None, dpi=192, verbose=False)

#m.bluemarble(alpha=0.8) # for natural color
#m.drawcoastlines(color='#000000', linewidth=1)
m.drawstates(color='#000000', linewidth=2)
#m.drawmapboundary(fill_color='#015876')
#m.fillcontinents(color='#f2f2f2',lake_color='#015876')
m.drawparallels(parallels,labels=[False,True,True,False])
m.drawmeridians(meridians,labels=[True,False,False,True])

ax.scatter(x=df['longitude'], y=df['latitude'], 
           s=df['frp'] / 10, label="Power",
           c=df['brightness'] / 10, cmap=plt.get_cmap("inferno"),
           alpha=0.5, zorder=10)
ax.set_title("Fire hazard in the last 24 hours ("+now.strftime("%Y-%m-%d %H:%M")+")")

fig.savefig('output_eosmodis_fires.png')
#plt.show()
exit()