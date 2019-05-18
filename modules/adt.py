import json
import urllib.request
import urllib.request
from folium import Map, Circle
import datetime

class Earthquake:
    """
    Class Earthquake which is used to present an object of class Earthquakes.
    """

    def __init__(self, earthquake):
        """

        :param earthquake:info about earthquake.
        """

        self.power = earthquake["properties"]["mag"]
        self.coordinates = earthquake["geometry"]["coordinates"]
        self.place = earthquake["properties"]["place"]
        if earthquake["properties"]["tsunami"]:
            self.reason = "tsunami"
        else:
            self.reason = None



class Earthquakes:
    def __init__(self, date):
        """
        Initialisation of different parameters
        date - date of earthquake
        """
        self.chance = {}
        self.places = {}
        self.place_damaged = {}
        self.place_min_damage = {}
        self.place_max_damage = {}
        self.place_reason = {}
        self.locations = {}
        self.date = date
        self.place_damaged = {}


    def get_earthquakes(self, date):
        """

        :param date: date of earthquakes.
        :return: dict of locations where earthquakes happen.

        (changes the class parameters)
        """

        helping = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + str(
            date[0]) + "-" + str(date[1]) + "-" + str(date[2]) + "&endtime=" + str(int(date[0] + 1)) + "-" + \
                  str(date[1]) + "-" + str(date[2])

        print(helping)
        earthquake_API = urllib.request.urlopen(helping)
        earthquake_API = earthquake_API.read().decode('utf-8')
        earthquakes = json.loads(earthquake_API)
        for earthquake in earthquakes["features"]:
            earth = Earthquake(earthquake)
            a = 0
            ngot = True
            for location in self.locations:
                a += 1
                if earth.coordinates[0] - 1 <= location[0] <= earth.coordinates[0] + 1 and \
                        earth.coordinates[1] - 1 <= location[1] <= earth.coordinates[1] + 1:
                    if earth.power:
                        if self.place_damaged[location]:
                            self.place_damaged[location] = (self.place_damaged[location] * self.locations[location] + earth.power) \
                                                           / (self.locations[location] + 1)
                        else:
                            self.place_damaged[(earth.coordinates[0], earth.coordinates[1])] = earth.power
                        self.locations[location] += 1

                    ngot = False
                    break
            if ngot:
                self.place_damaged[(earth.coordinates[0], earth.coordinates[1])] = earth.power
                self.locations[(earth.coordinates[0], earth.coordinates[1])] = 1

    def create_map(self):
        """
        Creates a map of earthquakes.

        """

        map1 = Map(tiles="Stamen Terrain")
        for i in self.locations:

            if self.place_damaged[i[0], i[1]] and self.place_damaged[i[0], i[1]] > 0.5:

                if self.place_damaged[i[0], i[1]] > 5\
                        :
                    a = 'darkred'
                    to_write = 'The earthquake damage here is really high.'
                elif self.place_damaged[i[0], i[1]] > 3.5:
                    a = 'red'
                    to_write = 'Might cause some destructions.'
                elif self.place_damaged[i[0], i[1]] > 1.5:
                    a = 'orange'
                    to_write = "Some ground shaking but would't cause some big troubles"
                else:
                    a = 'yellow'
                    to_write = "Almost nothing changed, but probably make some inconvenience to people"
                if len(self.date) == 1:
                    sized = 4
                elif len(self.date) == 2:
                    sized = 50
                elif len(self.date) == 3:
                    sized = 1500
                map1.add_child(Circle(
                    location=[i[1], i[0]],
                    popup=to_write,
                    radius= 10000 + sized * self.locations[i[0], i[1]],
                    color=a,
                    fill=True,
                    fill_color=a))
        map_name = "templates/Map_" + str(int(self.date[0]))

        if len(self.date) >= 2:
            map_name += '_' + str(int(self.date[1]))
        if len(self.date) == 3:
            map_name += "_" + str(int(self.date[2]))
        map_name += '.html'
        map1.save(map_name)

    def run(self):
        if len(self.date) == 3:
            self.get_earthquakes(self.date)
        elif len(self.date) == 2:
            if int(self.date[0]) in [1, 3, 5, 7, 8, 10, 12]:
                for d in range(1, 31):
                    self.get_earthquakes([d, self.date[0], self.date[1]])
            elif int(self.date[0]) in [4, 6, 9, 11]:
                for d in range(1, 30):
                    self.get_earthquakes([d, self.date[0], self.date[1]])
            elif int(self.date[0]) == 2:
                for d in range(1, 28):
                    self.get_earthquakes([d, self.date[0], self.date[1]])
        elif len(self.date) == 1:
            for m in range(1, 13):
                if m in [1, 3, 5, 7, 8, 10, 12]:
                    for d in range(1, 31):
                        self.get_earthquakes([d, m, self.date[0]])
                elif m in [4, 6, 9, 11]:
                    for d in range(1, 30):
                        self.get_earthquakes([d, m, self.date[0]])
                elif m == 2:
                    for d in range(1, 28):
                        self.get_earthquakes([d, m, self.date[0]])
        self.create_map()

    def get_prediction(self):
        """
        Logical assumption about nearest earthquakes based on last month - 2 month information.
        """


        now = datetime.datetime.now()
        now = list(map(int, str(now.date()).split('-')))
        now.reverse()
        days = 0
        if now[-2] in [2, 4, 6, 8, 9, 11]:
            for day in range(now[-3], 31):
                days += 1
                self.get_earthquakes_for_text([day, int(now[-2]) - 1, int(now[-1]) ])
        elif now[-2] == 3:
            for day in range(now[-3], 28):
                days += 1
                self.get_earthquakes_for_text([day, int(now[-2]) - 1, int(now[-1])])
        elif now[-2] == 1:
            for day in range(now[-3], 31):
                days += 1
                self.get_earthquakes_for_text([day, 12, int(now[-1]) - 1])
        else:
            for day in range(now[-3], 30):
                days += 1
                self.get_earthquakes_for_text([day, int(now[-2]) - 1, int(now[-1])])
        for day in range(1, int(now[-3])):
            days += 1
            self.get_earthquakes_for_text([day, int(now[-2]), int(now[-1])])
        map1 = Map()
        for place in self.places:
            if place in self.place_damaged:
                if self.place_damaged[place] - self.place_min_damage[place\
                        ] > self.place_max_damage[place] - self.place_damaged[place]:
                    self.place_damaged[place] = (self.place_damaged[place] + self.place_min_damage[place]) / 2
                elif place in self.place_damaged:
                    self.place_damaged[place] = (self.place_damaged[place] + self.place_min_damage[place]) / 2
                self.chance[place] = len(self.places[place]) / days
                if self.chance[place] > 0.1:
                    if self.place_damaged[place] > 0.5:
                        to_write = """"With chance {}% there would be earthquake in {} with probable power cl\
ose to {}""".format(str(self.chance[place])[0:3], place,  self.place_damaged[place])
                        if self.chance[place] > 0.8:
                            chances = 'darkred'
                        elif self.chance[place] > 0.6:
                            chances = 'red'
                        elif self.chance[place] > 0.4:
                            chances = 'orange'
                        else:
                            chances = 'yellow'
                        a = self.places[place][0].coordinates
                        map1.add_child(Circle(
                            location=[a[0], a[1]],
                            popup=to_write,
                            radius=10000,
                            color=chances,
                            fill=True,
                            fill_color=chances))
        map1.save('templates/Map_prediction.html')

    def get_earthquakes_for_text(self, date):
        """
        Change some init parameters forwarding text info to be written on users screen
        :param date: Date of earthquakes
        """
        helping = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + str(
            date[0]) + "-" + str(date[1]) + "-" + str(date[2]) + "&endtime=" + str(int(date[0] + 1)) + "-" + \
                  str(date[1]) + "-" + str(date[2])

        earthquake_API = urllib.request.urlopen(helping)
        earthquake_API = earthquake_API.read().decode('utf-8')
        earthquakes = json.loads(earthquake_API)
        for earthquake in earthquakes["features"]:
            earth = Earthquake(earthquake)
            if earth.power and earth.power > 0.5:
                if earth.place in self.places:
                    self.places[earth.place].append(earth)
                else:
                    self.places[earth.place] = [earth]

        reason = None
        for place in self.places:
            no_reason = True
            damage = 0
            for x in self.places[place]:

                if x.reason and no_reason:
                    self.place_reason[place] = x.reason
                    no_reason = False
                damage += x.power

                if place in self.place_max_damage and self.place_max_damage[place] < x.power:
                    self.place_max_damage[place] = x.power
                elif not place in self.place_max_damage:
                    self.place_max_damage[place] = x.power
                if place in self.place_min_damage and self.place_min_damage[place] > x.power:
                    self.place_min_damage[place] = x.power
                elif not place in self.place_min_damage:
                    self.place_min_damage[place] = x.power
            self.place_damaged[place] = damage/len(self.places[place])


    def run_text(self):
        """
        Text version of info about earthquakes.
        :return:
        """

        self.date = str(self.date)
        self.date = list(map(int, self.date.split('.')))
        if len(self.date) == 3:
            self.get_earthquakes_for_text(self.date)
        elif len(self.date) == 2:
            if int(self.date[0]) in [1, 3, 5, 7, 8, 10, 12]:
                for d in range(1, 31):
                    self.get_earthquakes_for_text([d, self.date[-2], self.date[-1]])
            elif int(self.date[0]) in [4, 6, 9, 11]:
                for d in range(1, 30):
                    self.get_earthquakes_for_text([d, self.date[-2], self.date[-1]])
            elif int(self.date[0]) == 2:
                for d in range(1, 28):
                    self.get_earthquakes_for_text([d, self.date[-2], self.date[-1]])
        elif len(self.date) == 1:
            for m in range(1, 13):
                if m in [1, 3, 5, 7, 8, 10, 12]:
                    for d in range(1, 31):
                        self.get_earthquakes_for_text([d, m, self.date[-1]])
                elif m in [4, 6, 9, 11]:
                    for d in range(1, 30):
                        self.get_earthquakes_for_text([d, m, self.date[-1]])
                elif m == 2:
                    for d in range(1, 28):
                        self.get_earthquakes_for_text([d, m, self.date[-1]])
        text_name = "templates/Text_" + str(int(self.date[0]))
        if len(self.date) >= 2:
            text_name += '_' + str(int(self.date[1]))
        if len(self.date) == 3:
            text_name += "_" + str(int(self.date[2]))
        text_name += '.html'
        file = open(text_name, 'w+')
        file.write('<head><meta charset="utf-8" /><title>ERROR</title><STYLE type="text/css">body {background:\
rgba(53, 53, 53, 0.92) \
url("https://d2v9y0dukr6mq2.cloudfront.net/video/thumbnail/SsOzHoGozjflh6xor/videoblocks-ground-splitting-during-an-earthquake-3d-rendering_h-irx8njm_thumbnail-full14.png") \
fixed;background-repeat: no-repeat;}h2 {color: ghostwhite;}h3 {color: red;}</STYLE></head>')
        file.write('<body>')
        total_earthquakes = 0
        total_avg_damage = 0
        k = 0
        for place in self.places:
            print(1)
            k += 1
            if place in self.place_damaged:
                total_avg_damage += self.place_damaged[place]
            total_earthquakes += len(self.places[place])
            if place in self.place_damaged:
                file.write('<h3>Place: {}. The amount of earthquakes there: {}. The average power of earthquakes here: {}\
with max power: {} and min power: {}'.format(place, len(self.places[place]), self.place_damaged[place],
                                             self.place_max_damage[place], self.place_min_damage[place]))
            if place in self.place_reason:
                file.write('and some of them were caused by tsunami.</h3>')

        avg_damage = total_avg_damage / k
        file.write('<h2>The total amount of earthquakes around the world that day was {} with average power {}.'.format(
            total_earthquakes, avg_damage))
        file.write('.</h2>')
        file.write('</body')
        file.close()
