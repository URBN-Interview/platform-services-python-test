#!/usr/bin/env python
# Entry point for the RewardsService API.
# Builds the Tornado application from the routes in url_patterns.py and the
# config in settings.py, then starts an HTTP server on the configured port (7050).

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import motor.motor_tornado

from tornado.options import options

from settings import settings
from url_patterns import url_patterns


class App(tornado.web.Application):
    """Tornado application for the rewards API.

    Wires the URL routes to their handlers and applies the settings dict.
    Shared resources (e.g. a database client) can be attached here so every
    handler can reach them via self.application.
    """

    def __init__(self, urls):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db = motor.motor_tornado.MotorClient("mongodb", 27017)["Rewards"]
        
        tornado.web.Application.__init__(self, urls, **settings)

app = App(url_patterns)


def main():
    logger = logging.getLogger()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    logger.info('Tornado server started on port {}'.format(options.port))

    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logger.info("\nStopping server on port {}".format(options.port))


if __name__ == "__main__":
    main()
