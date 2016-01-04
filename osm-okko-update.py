#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: error reporting

import xml.etree.ElementTree as ET
import urllib.request as URL
import sys, math
from osmapi import OsmApi as OSM

# Log into OSM
login = input("OSM Login: ")
passwd = input("OSM Password: ")
osm = OSM(login, passwd)

# Calculations stolen from: http://msi.nga.mil/MSISiteContent/StaticFiles/Calculators/degree.html
m1 = 111132.92
m2 = -559.82
m3 = 1.175
m4 = -0.0023
p1 = 111412.84
p2 = -93.5
p3 = 0.118

# Length of a latitude degree on a given latitude
def latm(lat):
    latr = math.radians(lat)
    return m1 + (m2 * math.cos(2 * latr)) + (m3 * math.cos(4 * latr)) + (m4 * math.cos(6 * latr))

# Length of a longitude degree on a given latitude
def lonm(lat):
    latr = math.radians(lat)
    return (p1 * math.cos(latr)) + (p2 * math.cos(3 * latr)) + (p3 * math.cos(5 * latr))

# Adds the namespace bit to the tag, convenience
def _NS(txt):
    return "{http://www.topografix.com/GPX/1/1}"+txt

# Separate function to reduce visual litter
def is_fuel_station(item):
    return "type" in item and item["type"]=="node" and "data" in item and "tag" in item["data"] and "amenity" in item["data"]["tag"] and item["data"]["tag"]["amenity"]=="fuel"

# Process a fuel station entry
def processStation(entry):
    global osm
    lon = float(entry.attrib["lon"])
    lat = float(entry.attrib["lat"])
    meters = 50 # How much meters to search around the point

    print("Station in the list: "+str(lon)+" "+str(lat))

    mp = osm.Map(lon - meters/lonm(lat), lat - meters/latm(lat), lon + meters/lonm(lat), lat + meters/latm(lat))

    # TODO replace with predicate after we learn how to edit stations
    okko_found = 0
    for item in mp:
        if is_fuel_station(item):
            okko_found += 1
    print("Fuel stations found: "+str(okko_found))

# Load the XML
data = len(sys.argv) > 1 and sys.argv[1] or URL.urlopen('http://www.okko.ua/uploads/doc/map/okko.gpx')
tree = ET.parse(data)
root = tree.getroot()

# Go!
[processStation(x) for x in root if x.tag==_NS("wpt")]
