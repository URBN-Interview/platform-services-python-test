#!/usr/bin/env python
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options

from settings import settings
from url_patterns import url_patterns


class App(tornado.web.Application):
    """
    Custom Tornado Application class.

    Inherits from tornado.web.Application and initializes with given URL patterns and settings.
    """

    def __init__(self, urls):
        """
        Initialize the Tornado application.

        Args:
            urls (list): List of URL patterns to be used by the application.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__(urls, **settings)


def main():
    """
    Main function to start the Tornado web server.
    """
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # Parse command line options
    tornado.options.parse_command_line()

    # Create HTTP server instance
    http_server = tornado.httpserver.HTTPServer(App(url_patterns), xheaders=True)
    http_server.listen(options.port)

    # Log server start
    logger.info('Tornado server started on port {}'.format(options.port))

    try:
        # Start the event loop
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        # Gracefully stop the server on Keyboard Interrupt
        logger.info("\nStopping server on port {}".format(options.port))


if __name__ == "__main__":
    main()

