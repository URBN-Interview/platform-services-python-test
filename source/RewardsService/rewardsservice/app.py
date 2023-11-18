#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import options

from settings import settings
from url_patterns import url_patterns


class App(tornado.web.Application):
    def __init__(self, urls):
        self.logger = logging.getLogger(self.__class__.__name__)

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
