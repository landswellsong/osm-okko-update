#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: error reporting

import xml.etree.ElementTree as ET
import urllib.request as URL
import sys

# Adds the namespace bit to the tag, convenience
def _NS(txt):
    return "{http://www.topografix.com/GPX/1/1}"+txt

# Process a fuel station entry
def processStation(entry):
    print("Station found: "+str(entry.attrib["lon"])+" "+str(entry.attrib["lat"]))

# Load the XML
data = len(sys.argv) > 1 and sys.argv[1] or URL.urlopen('http://www.okko.ua/uploads/doc/map/okko.gpx')
tree = ET.parse(data)
root = tree.getroot()

# Go!
[processStation(x) for x in root if x.tag==_NS("wpt")]
