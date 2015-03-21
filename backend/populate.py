#!/bin/env python
#
# This script reads POIs and categoris scraped from bastogne.be website to create entries in a MySQL database.
#

from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from sqlalchemy import create_engine
from settings import *
import json
import random

if __name__ == "__main__":

    print "[+] Populating data to the database ..."

    try:
        engine = create_engine("mysql://%s:%s@%s/%s?charset=utf8" % (db_username, db_password, db_host, db_name),
                               encoding='utf-8', echo=False)
        db = scoped_session(sessionmaker(bind=engine))
        print "[+] Cleaning up previous dataset ..."
        db.query(POI).delete()
        db.query(Category).delete()

        pois = json.load(open("pois.json"))
        for p in pois:
            poi = POI(name=p["name"], description=p["description"], url="http://google.be", latitude=p["lat"],
                      longitude=p["lon"], qrcode="")
            db.add(poi)

        categories = ["Default", "Batiments publics", "Arts et culture", "Loisirs", "Artisanat", "Patrimoine", "Nature",
                      "Commerce", "Sport", "Tourisme"]
        for c in categories:
            category = Category(name=c, description="")
            db.add(category)

        category = db.query(Category).filter(Category.name == "Default").scalar()
        pois = db.query(POI).all()
        for p in pois:
            p.category = category

        for i in range(0, 10):
            trail = Trail(name="test %d" % i, description="description test %d" % i)
            for _ in range(0, 10):
                poi = db.query(POI).filter(POI.id == random.randint(pois[0].id, pois[0].id + len(pois))).scalar()
                if poi is not None:
                    trail.pois.append(poi)
            db.add(trail)
        db.commit()

        print "[+] Done !"

    except Exception as e:
        print "[!] Shit, something happened. %s" % e
