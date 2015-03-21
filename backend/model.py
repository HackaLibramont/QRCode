#!/bin/env python
#
# SQLAlchemy models
#
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey, BLOB
from sqlalchemy.orm import relationship, backref
engine = create_engine('mysql://qrcode:_Mx1VzNxLeeU1LQh@localhost/qrcode?charset=utf8', encoding='utf-8', echo=False)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class POIPicture(Base):
    __tablename__ = 'picture_poi_link'
    id = Column(Integer, primary_key=True)
    poi_id = Column(Integer, ForeignKey('poi.id'), primary_key=True)
    picture_id = Column(Integer, ForeignKey('picture.id'), primary_key=False)


class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    path = Column(String(30), nullable=False)

    pois = relationship(
        'POI',
        secondary='picture_poi_link'
    )
    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path
        }

class POI(Base):
    __tablename__ = 'poi'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(30), nullable=True)
    url = Column(String(30), nullable=True)
    latitude = Column(Float(), nullable=True)
    longitude = Column(Float(), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", backref="poi")
    qrcode = Column(BLOB(), nullable=False)
    pictures = relationship("POIPicture", backref="poi")

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "category": self.category.as_json(),
            "qrcode": self.qrcode,
            "pictures": [p.as_json() for p in self.pictures]
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(30), nullable=True)

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class TrailPOI(Base):
    __tablename__ = 'trail_poi_link'
    id = Column(Integer, primary_key=True)
    trail_id = Column(Integer, ForeignKey('trail.id'), primary_key=False)
    poi_id = Column(Integer, ForeignKey('poi.id'), primary_key=False)


class Trail(Base):
    __tablename__ = 'trail'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(30), nullable=True)
    tags = Column(String(30), nullable=True)
    pois = relationship(
        'POI',
        secondary='trail_poi_link'
    )

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "pois": [p.as_json() for p in self.pois]
        }

pois_table = POI.__table__
categories_table = Category.__table__
trails_table = Trail.__table__
trail_poi_links_table = TrailPOI.__table__
picture_poi_links_table = POIPicture.__table__
metadata = Base.metadata


def drop_all():
    metadata.drop_all(engine, tables=[pois_table, categories_table, trails_table, trail_poi_links_table, picture_poi_links_table])


def create_all():
    metadata.create_all(engine, tables=[pois_table, categories_table, trails_table, trail_poi_links_table, picture_poi_links_table])