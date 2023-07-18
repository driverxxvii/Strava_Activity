import geopy.distance
from bs4 import BeautifulSoup
from datetime import datetime


class Activity:
    def __init__(self, file_name):
        # file_name is the full path of the gpx file
        self.file_name = file_name
        self.soup = self.soupify()
        self.activity_date, self.start_time, self.finish_time = \
            self.activity_date_and_time()
        self.get_distance()

    def soupify(self):
        with open(self.file_name, "r") as f:
            file_contents = f.read()

        soup = BeautifulSoup(file_contents, features="xml")
        return soup

    def activity_date_and_time(self):
        start_date_time = self.soup.find("time").text  # 2023-07-17T20:02:20Z
        finish_date_time = self.soup.findAll("time")[-1].text

        # create datetime objects
        start_date_time = datetime.strptime(start_date_time,
                                            "%Y-%m-%dT%H:%M:%S%z")
        finish_date_time = datetime.strptime(finish_date_time,
                                             "%Y-%m-%dT%H:%M:%S%z")

        activity_date = start_date_time.date()
        start_time = start_date_time.time()
        finish_time = finish_date_time.time()
        return activity_date, start_time, finish_time

    def get_distance(self):
        # get coordinates of points
        coords = []
        for point in self.soup.findAll("trkpt"):
            #    <trkpt lat="51.3868060" lon="0.0378420">
            lat = float(point["lat"])
            lon = float(point["lon"])

            coord_tuple = tuple([lat, lon])
            # coords is a list of (lat, lon) tuples
            coords.append(coord_tuple)

        total_distance = 0
        for i, item in enumerate(coords[:-1]):
            coord1 = item
            coord2 = coords[i + 1]
            dist = geopy.distance.distance(coord1, coord2).m
            total_distance += dist

        # returned distance is in metres
        self.distance = total_distance


def main():
    file_name = r"C:\Users\User1\Desktop\Temp\Strava\Night_Ride.gpx"
    bike = Activity(file_name)
    print(bike.activity_date)
    print(bike.start_time)
    print(bike.finish_time)
    print(bike.distance)


if __name__ == "__main__":
    main()
