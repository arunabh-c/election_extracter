import numpy as np
from shapely.geometry import Point, shape
from geopandas import read_file
from xml.etree import ElementTree
import shapely.speedups
import keytree
import time

shapely.speedups.enable()
federal_geojson = read_file("districts.geojson")
federal_kml = open("cb_2018_us_cd116_500k.kml").read()
state_house_geojson = read_file("CA/HOUSE/Legislative_Districts_in_California.geojson")
state_senate_geojson = read_file("CA/SENATE/Legislative_Districts_in_California.geojson")
state_school_geojson = read_file("CA/SCHOOL/California_School_District_Areas_2020-21.geojson")

def get_district_json(point: Point, file: str) -> str:
    index = np.where(file.contains(point))[0]
    return file.values[index][0][0]

def get_district_kml(point: Point, file: str) -> str:
     tree = ElementTree.fromstring(file)
     kmlns = tree.tag.split('}')[0][1:]
     
     # Find all Polygon elements anywhere in the doc
     elems = tree.findall(".//{%s}Polygon" % kmlns)
     # Filter polygon elements using this lambda (anonymous function)
     # keytree.geometry() makes a GeoJSON-like geometry object from an
     # element and shape() makes a Shapely object of that.
     #cds = tree.findall(".//{%s}Polygon" % kmlns)
     #for item in elems:
         #print(item.Polygon)
         #if item.contains(point):
           #print(item)
     hits = filter(lambda e: shape(keytree.geometry(e)).contains(point),elems )
     #print(file)
     #index = np.where(keytree.geometry(e)).contains(point)[0]
     #return list(hits)[0]
     print(len(elems))
     print(elems[elems.index(list(hits)[0])-1])
     return elems.index(list(hits)[0])
     
 
def find_district(lat, long):
        point = Point(float(lat), float(long))
        print(get_district_kml(point,federal_kml))
        # print(get_district_json(point,federal_geojson))
        # print(get_district_json(point,state_house_geojson))
        # print(get_district_json(point,state_senate_geojson))
        # print(get_district_json(point,state_school_geojson))

start = time.time()
 
find_district(-122.171520,37.448740)

end = time.time()
print("Time taken in seconds: " + str(end - start))
