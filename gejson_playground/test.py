import numpy as np
from shapely.geometry import Point, shape, Polygon, LineString
from geopandas import read_file
import keytree
import time
import xml.etree.ElementTree as ET

namespaces = {'owl': 'http://www.opengis.net/kml/2.2'}

# federal_geojson = read_file("districts.geojson")
# fed_kml_file = "cb_2018_us_cd116_500k.kml"
# federal_kml = open(fed_kml_file).read()
state_kml_file = "CA/SENATE/Legislative_Districts_in_California.kml"
state_senate_kml = open(state_kml_file).read()
#print(state_kml)
# state_house_geojson = read_file("CA/HOUSE/Legislative_Districts_in_California.geojson")
#state_senate_geojson = read_file("CA/SENATE/Legislative_Districts_in_California.geojson")
# state_school_geojson = read_file("CA/SCHOOL/California_School_District_Areas_2020-21.geojson")

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
     return 0#elems.index(list(hits)[0])
     
def contains_location(kml_file, point):
    # Parse the KML file
    tree = ET.parse(kml_file)
    root = tree.getroot()
    #print(tree)
    # Find the Placemark element
    all_placemarks = root.findall(".//{http://www.opengis.net/kml/2.2}Placemark")
    #print(all_placemarks)
    #print(len(all_placemarks))
    ctr = 0
    for placemark in all_placemarks:
       # if placemark is None:
         # return False
       print(ctr)
       # Find the Polygon element
       polygon = placemark.find(".//{http://www.opengis.net/kml/2.2}Polygon")
       #print(polygon)
       #print(len(polygon))
       # if polygon is None:
         # return False
       # Parse the coordinates of the polygon
       coords = polygon.find(".//{http://www.opengis.net/kml/2.2}coordinates").text
       #print(coords)
       coords = [tuple(map(float, coord.split(","))) for coord in coords.split()]
       #print(coords)

       # Check if the location is contained in the polygon
       poly = Polygon(coords)
       line = LineString(coords)
       polyg = Polygon(line)
       #print("hehe")
       #print(poly.area)
       #print(poly.is_valid)
       #poin
       point = Point(-122.17153053064935, 37.449057797528155)
       # if (point.within(polygon)):
          # print(point.within(polygon))
       print(point.distance(polyg))
       if point.intersects(polyg):
         return True
       if polyg.contains(point):
         return True
       ctr += 1
    print(ctr)
    return False

def find_district(lat, long):
        point = Point(float(lat), float(long))
        if contains_location(state_kml_file, point):
          print("The location is contained within the Placemark's Polygon")
        else:
          print("The location is not contained within the Placemark's Polygon")
        #print(contains_location(federal_kml,point))
        #print(get_district_kml(point,federal_kml))
        # print(get_district_json(point,federal_geojson))
        # print(get_district_json(point,state_house_geojson))
        #print(get_district_json(point,state_senate_geojson))
        # print(get_district_json(point,state_school_geojson))

start = time.time()
find_district(-122.17151792916684,37.44872114728699)
end = time.time()
print("Time taken in seconds: " + str(end - start))
