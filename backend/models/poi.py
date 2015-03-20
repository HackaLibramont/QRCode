#!/bin/env python

class Category:
    """
    POI category.
    """
    def __init__(self, id=0, name=None, description=None):
        self._id = id
        self._name = name
        self._description = description

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value


class POI:
    """
    Point of Interest.
    """

    def __init__(self, id=0, name=None, description=None, latitude=0.0, longitude=0.0, category=None, qr=None,
                 pictures=None):
        self._id = id
        self._name = name
        self._description = description
        self._latitude = latitude
        self._longitude = longitude
        self._category = category
        self._qr = qr
        self._pictures = pictures

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def qr(self):
        return self._qr

    @qr.setter
    def qr(self, value):
        self._qr = value

    @property
    def pictures(self):
        return self._pictures

    @pictures.setter
    def pictures(self, value):
        self._pictures = value