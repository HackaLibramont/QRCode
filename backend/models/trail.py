#!/bin/env python


class Trail:
    """
    A trail is composed of multiple POI by which a user will pass by.
    """

    def __init__(self, id=0, name=None, description=None, tags=None, pois=None):
        self._id = id
        self._name = name
        self._description = description
        self._tags = tags
        self._pois = pois

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
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    @property
    def pois(self):
        return self._pois

    @pois.setter
    def pois(self, value):
        self._pois = value


