import json
import urllib.request
import urllib.request
from folium import Map, CircleMarker, Marker

map = Map()

earthquake_API = urllib.request.urlopen("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-02&endtime=2014-01-03")
earthquake_API = earthquake_API.read().decode('utf-8')
earthquake = json.loads(earthquake_API)
for i in earthquake["features"]:
    map.add_child(CircleMarker(location=[-180, 180],
                                              popup="Test",
                                              color = "brown",
                                              fill_opacity = 0.3,
                                              radius=20,
                                              fill_color = "red"))

    break

map.save('Map_1.html')
