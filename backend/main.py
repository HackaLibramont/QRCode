#!/usr/bin/env python

import json

import tornado.autoreload
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import os
import torndb
from tornado.options import define, options
import os
import sys
LISTENERS = []


class MainHandler(tornado.web.RequestHandler):
    """Point-of-interest handler

    """

    def get(self):
        self.write("QRCode")


class PoisHandler(tornado.web.RequestHandler):
    """Point-of-interest handler

    """

    def get(self):
        raise Exception("Not yet implemented.")

    def post(self):
        raise Exception("Not yet implemented.")

    def delete(self):
        raise Exception("Not yet implemented.")


class PoiHandler(tornado.web.RequestHandler):
    """Point-of-interest handler

    """

    def get(self):
        raise Exception("Not yet implemented.")

    def post(self):
        raise Exception("Not yet implemented.")

    def delete(self):
        raise Exception("Not yet implemented.")


class TrailsHandler(tornado.web.RequestHandler):
    """Point-of-interest handler

    """

    def get(self):
        raise Exception("Not yet implemented.")

    def post(self):
        raise Exception("Not yet implemented.")

    def delete(self):
        raise Exception("Not yet implemented.")


class TrailHandler(tornado.web.RequestHandler):
    """Point-of-interest handler

    """

    def get(self):
        raise Exception("Not yet implemented.")

    def post(self):
        raise Exception("Not yet implemented.")

    def delete(self):
        raise Exception("Not yet implemented.")


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
            (r'/poi/', PoisHandler),
            (r'/poi/(\d+)/', PoiHandler),
            (r'/trail/', TrailsHandler),
            (r'/trail/(\d+)/', TrailHandler)
        ]

        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )
        super(Application, self).__init__(handlers, **settings)





if __name__ == '__main__':

    if os.path.exists("config.json"):
        with open("config.json", "rb") as f:
            config = json.load(f)

        define("mysql_host", default="%s:%d" % (config["database"]["host"], config["database"]["port"]))
        define("mysql_database", default=config["database"]["name"])
        define("mysql_user", default=config["database"]["username"])
        define("mysql_password", default=config["database"]["password"])

        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(config["server"]["port"])
        print "[+] Starting server on %s:%d" % (config["server"]["ip"], config["server"]["port"])
        tornado.ioloop.IOLoop.instance().start()
    else:
        raise Exception("Config file not found.")