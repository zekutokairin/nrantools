#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import untangle

XMLFILE = "ArcadeMusic.xml"

#tree = ET.parse(XMLFILE)
#root = tree.getroot()

obj = untangle.parse(XMLFILE)

import code
code.interact(local=locals())

