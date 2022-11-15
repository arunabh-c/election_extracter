import numpy as np
from shapely.geometry import Point
from geopandas import read_file

GEOJSON = read_file("districts.geojson")

def get_federal_district(index: int) -> str:
    return GEOJSON.values[index][0][0]

def find_district(lat, long):
        point = Point(float(lat), float(long))
        index = np.where(GEOJSON.contains(point))[0]
        print(get_federal_district(index))

find_district(-122.171520,37.448740)