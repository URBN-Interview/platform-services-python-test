#!/usr/bin/env python
import logging

import motor.motor_tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import options

from repository import RewardsRepository
from settings import MONGO_DB, MONGO_HOST, MONGO_PORT, settings
from url_patterns import make_url_patterns


class App(tornado.web.Application):
    def __init__(self, repository, **overrides):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.repository = repository

        tornado.web.Application.__init__(self, make_url_patterns(repository), **{**settings, **overrides})


def main():
    logger = logging.getLogger()
    tornado.options.parse_command_line()

    client = motor.motor_tornado.MotorClient(MONGO_HOST, MONGO_PORT)
    repository = RewardsRepository(client[MONGO_DB])
    app = App(repository)

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.current().run_sync(repository.ensure_indexes)
    except Exception:
        logger.exception("Could not create MongoDB indexes; continuing without them")

    logger.info('Tornado server started on port {}'.format(options.port))

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logger.info("\nStopping server on port {}".format(options.port))


if __name__ == "__main__":
    main()
