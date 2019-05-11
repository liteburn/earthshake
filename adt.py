import json
import urllib.request
import urllib.request
from folium import Map, Circle


class Earthquake:
    def __init__(self, earthquake):
        self.power = earthquake["properties"]["mag"]
        self.coordinates = earthquake["geometry"]["coordinates"]
        self.place = earthquake["properties"]["place"]
        if earthquake["properties"]["tsunami"]:
            self.reason = "tsunami"
        else:
            self.reason = None


class Earthquakes:
    def __init__(self, date):
        self.locations = {}
        if len(date) == 3:
            self.get_earthquakes(date)
        elif len(date) == 2:
            if int(date[0]) in [1, 3, 5, 7, 8, 10, 12]:
                for k in range(0,31):
                    self.get_earthquakes([k, date[0], date[1]])
            elif int(date[0]) in [4, 6, 9, 11]:
                for k in range(0,30):
                    self.get_earthquakes([k, date[0], date[1]])
            elif int(date[0]) == 2:
                for k in range(0, 28):
                    self.get_earthquakes([k, date[0], date[1]])
        elif len(date) == 1:
            for m in range(1, 13):
                if m in [1, 3, 5, 7, 8, 10, 12]:
                    for k in range(0, 31):
                        self.get_earthquakes([m, k, date[0]])
                elif m in [4, 6, 9, 11]:
                    for k in range(0, 30):
                        self.get_earthquakes([m, k, date[0]])
                elif m == 2:
                    for k in range(0, 28):
                        self.get_earthquakes([m, k, date[0]])


    def get_earthquakes(self, date):
        helping = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + str(
            date[0]) + "-" + str(date[1]) + "-" + str(date[2]) + "&endtime=" + str(int(date[0]) + 1) + "-" + \
                  str(date[1]) + "-" + str(date[2])
        print(helping)
        earthquake_API = urllib.request.urlopen(helping)
        earthquake_API = earthquake_API.read().decode('utf-8')
        earthquakes = json.loads(earthquake_API)
        for earthquake in earthquakes["features"]:
            earth = Earthquake(earthquake)
            a = 0
            for location in self.locations:
                a += 1
                if earth.coordinates[0] - 1 <= location[0] <= earth.coordinates[0] + 1 and \
                        earth.coordinates[1] - 1 <= location[1] <= earth.coordinates[1] + 1:
                    self.locations[location].append(earth)
                    break
            if a == len(self.locations):
                self.locations[(earth.coordinates[0], earth.coordinates[1])] = [earth]

    def create_map(self, date):
        map1 = Map()
        for i in self.locations:
            map1.add_child(Circle(
                location=[i[1], i[0]],
                popup=str([x.place for x in self.locations[i[0], i[1]]]),
                radius= 10000,
                color='crimson',
                fill=True,
                fill_color='crimson'))
        print(int(date[0]), date[1], date[2])
        map_name = "template/Map_" + str(int(date[0]))

        if len(date) >= 2:
            map_name += '_' + str(int(date[1]))
        if len(date) == 3:
            map_name += "_" + str(int(date[2]))
        map_name += '.html'
        map1.save(map_name)
