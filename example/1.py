import json
import urllib.request
import urllib.request
from folium import Map, CircleMarker, Marker

map = Map()

DOTA_API = urllib.request.urlopen("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-03")
DOTA_API = DOTA_API.read().decode('utf-8')
DOTA = json.loads(DOTA_API)
for i in DOTA["features"]:
    map.add_child(CircleMarker(location=[i["geometry"]["coordinates"][1], i["geometry"]["coordinates"][0]],
                                              popup="Test",
                                              color = "brown",
                                              fill_opacity = 0.3,
                                              radius=20,
                                              fill_color = "red"))

    break

map.save('Map_1.html')
