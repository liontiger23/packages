#!/usr/bin/env python3

#  gettag.py: Get git tag for package
#
#  Copyright 2015 Ikey Doherty <iikey@solus-project.com>
#  Copyright 2024 Solus Developers <releng@getsol.us>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

import sys
import xml.etree.ElementTree as ET

from ruamel.yaml import YAML


def getYmlTag(spec):
    y = None
    try:
        yaml = YAML(typ="safe")
        with open(spec, "r") as f:
            y = yaml.load(f)
    except Exception as e:
        print(f"Unable to load {spec}: {e}")
        sys.exit(1)

    source = y["name"]
    version = y["version"]
    release = y["release"]

    print(f"{source}-{version}-{release}")


def getSpecTag(spec):
    tree = ET.parse(spec)
    root = tree.getroot()

    source = root.findall("Source")
    name = source[0].findall("Name")[0].text
    hist = root.findall("History")
    last_update = hist[0].findall("Update")[0]
    rel = str(last_update.attrib["release"])
    vers = str(last_update.findall("Version")[0].text)
    print(f"{name}-{vers}-{rel}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1].endswith(".yml"):
            getYmlTag(sys.argv[1])
        elif sys.argv[1].endswith("pspec.xml"):
            getSpecTag(sys.argv[1])
        else:
            print(("Invalid argument: %s" % sys.argv[1]))
            sys.exit(1)
        sys.exit(0)
    else:
        print("Invalid usage")
        sys.exit(1)
