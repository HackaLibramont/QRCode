"""
"""

import re
import urllib2
import json
import codecs


class Category(object):
    def __init__(self, name="", icon=None):
        self.name = name
        self.icon = icon

    def __eq__(self, other):
        return self.name == other.name


class Icon(object):
    def __init__(self, name="", url="", width=0, height=0):
        self.name = name
        self.url = url
        self.width = width
        self.height = height
        self.content = None

    def load(self):
        req = urllib2.Request(self.url)
        try:
            resp = urllib2.urlopen(req)
            self.content = resp.read()
        except urllib2.URLError, e:
            print e

    def save(self):
        if self.content is None:
            self.load()
            with open("%s.png" % (self.name), 'wb') as f:
                f.write(self.content)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.url == other.url and
            self.width == other.width and
            self.height == other.height
        )


class POI(object):
    def __init__(self, name="", description="", url="",
                 lat=0, lon=0, category=None):
        self.name = name
        self.description = description
        self.url = url
        self.category = category.__dict__
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.description == other.description and
            self.url == other.url and
            self.category == other.category and
            self.lat == other.lat and
            self.lon == other.lon
        )


if __name__ == "__main__":
    url = "http://bastogne.be/plan-de-bastogne/plan-de-bastogne"
    print "[$] parsing %s " % (url)

    pois = []
    categories = []
    icons = []
    req = urllib2.Request(url)
    try:
        resp = urllib2.urlopen(req)
        content = resp.read()
        matches = re.findall(
            r"""icon = createIcon\('(.*?)'\);clustererIcon = null;\ngicons\['(.*?)'\]""",
            content)

        matches = re.findall(
            r"""mgr\.addMarker\(createMarker\("(.*?)",new google.maps.LatLng\((\d+\.\d*),(\d+\.\d*)\),"(.*?)","(.*?)","(.*?)","(.*?)"\)\);""",
            content)
        for match in matches:
            category = Category(name="%s%s" % (match[6][0], match[6][1:].lower()))
            if category not in categories:
                categories.append(category)

            poi = POI(name=match[3].decode("utf-8"), description=re.sub('<[^<]+?>', '', match[4]).decode("utf-8"),
                      url=match[4], lat=float(match[1]),
                      lon=float(match[2]), category=category)
            pois.append(poi)
        with codecs.open("pois.json", "wb", "utf-8") as f:
            f.write(json.dumps([x.__dict__ for x in pois]))
        with codecs.open("categories.json", "wb", "utf-8") as f:
            f.write(json.dumps([x.__dict__ for x in categories]))

        print "[$] %d categories" % (len(categories))
        print "[$] %d pois" % (len(pois))

    except Exception, e:
        print e
