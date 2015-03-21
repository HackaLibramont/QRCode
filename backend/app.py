#!/usr/bin/env python

import json

import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os
from sqlalchemy.orm import scoped_session, sessionmaker
from model import *
from settings import *
import datetime
import StringIO
import qrcode
import base64
from math import radians, cos, sin, asin, sqrt


LISTENERS = []


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


class JSONEncoder(json.JSONEncoder):
    """
    Wrapper class to try calling an object's tojson() method. This allows
    us to JSONify objects coming from the ORM. Also handles dates and datetimes.
    """

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        try:
            return obj.as_json()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class MainHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self):
        self.write("QRCode documentation coming up soon.")


class PoisHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self):
        category_id = self.get_argument("category", default=None, strip=False)
        longitude = self.get_argument("longitude", default=0, strip=False)
        latitude = self.get_argument("latitude", default=0, strip=False)
        radius = self.get_argument("radius", default=500000, strip=False)
        if category_id is not None:
            pois = self.db.query(POI).filter(POI.category_id == category_id).all()
        else:
            pois = self.db.query(POI).all()

        pois = [p for p in pois if haversine(float(p.longitude), float(p.latitude), float(longitude), float(latitude)) < float(radius)]
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(pois, cls=JSONEncoder))

    def put(self):
        raise Exception("Not yet implemented.")


class PoiHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self, id):
        poi = self.db.query(POI).filter(POI.id == id).scalar()
        if poi is None:
            self.send_error(404)
        else:
            self.set_header("Content-Type", "application/json")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(json.dumps(poi, cls=JSONEncoder))

    def post(self, id):
        raise Exception("Not yet implemented.")

    def delete(self, id):
        poi = self.db.query(POI).filter(POI.id == id).scalar()
        if poi is None:
            self.send_error(404)
        else:
            if self.db.delete(poi):
                self.write()
            else:
                self.write_error(500, "The server encountered an error when deleting the POI.")


class PoiQRHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self, id):
        poi = self.db.query(POI).filter(POI.id == id).scalar()
        if poi is None:
            self.send_error(404)
        else:
            self.set_header("Access-Control-Allow-Origin", "*")
            output = StringIO.StringIO()
            img = qrcode.make("http://%s:%d/poi/%d/qr" % (ip, port, int(id)))
            img.save(output)
            content = base64.b64encode(output.getvalue())
            self.write("<img alt=\"QR code\" src=\"data:image/png;base64,%s\" />" % (content))


class TrailsHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self):
        trails = self.db.query(Trail).all()
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(trails, cls=JSONEncoder))

    def put(self):
        raise Exception("Not yet implemented.")


class TrailHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self, id):
        trail = self.db.query(Trail).filter(Trail.id == id).scalar()
        if trail is None:
            self.send_error(404)
        else:
            self.set_header("Content-Type", "application/json")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(json.dumps(trail, cls=JSONEncoder))

    def post(self, id):
        raise Exception("Not yet implemented.")

    def delete(self, id):
        trail = self.db.query(Trail).filter(Trail.id == id).scalar()
        if trail is None:
            self.send_error(404)
        else:
            if self.db.delete(trail):
                self.write()
            else:
                self.write_error(500, "The server encountered an error when deleting the trail.")


class CategoriesHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self):
        categories = self.db.query(Category).all()
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(categories, cls=JSONEncoder))

    def put(self):
        raise Exception("Not yet implemented.")


class CategoryHandler(BaseHandler):
    """Point-of-interest handler

    """

    def get(self, id):
        category = self.db.query(Category).filter(Category.id == id).scalar()
        if category is None:
            self.send_error(404)
        else:
            self.set_header("Content-Type", "application/json")
            self.set_header("Access-Control-Allow-Origin", "*")
            self.write(json.dumps(category, cls=JSONEncoder))

    def post(self, id):
        raise Exception("Not yet implemented.")

    def delete(self, id):
        category = self.db.query(Category).filter(Category.id == id).scalar()
        if category is None:
            self.send_error(404)
        else:
            if self.db.delete(category):
                self.write()
            else:
                self.write_error(500, "The server encountered an error when deleting the category.")


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            cookie_secret="5725af95ef74805b753cd3689bb3393681e02ce6",
            static_path="%s/static" % os.path.dirname(__file__),
            xsrf_cookies=True,
        )

        handlers = [
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
            (r'/', MainHandler),
            (r'/poi/?', PoisHandler),
            (r'/poi/(\d+)/?', PoiHandler),
            (r'/poi/(\d+)/qr/?', PoiQRHandler),
            (r'/trail/?', TrailsHandler),
            (r'/trail/(\d+)/?', TrailHandler),
            (r'/category/?', CategoriesHandler),
            (r'/category/(\d+)/?', CategoryHandler)
        ]
        self.db = scoped_session(sessionmaker(bind=engine))
        super(Application, self).__init__(handlers, **settings)

if __name__ == '__main__':

    define("mysql_host", default="%s:%d" % (db_host, db_port))
    define("mysql_database", default=db_name)
    define("mysql_user", default=db_username)
    define("mysql_password", default=db_password)

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    print "[+] Starting server on %s:%d" % (ip, port)
    tornado.ioloop.IOLoop.instance().start()