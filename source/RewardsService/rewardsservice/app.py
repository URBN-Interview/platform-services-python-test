#!/usr/bin/env python
import asyncio
import logging
import signal

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import options

from pymongo import AsyncMongoClient

from settings import settings
from url_patterns import build_url_patterns

from repositories.rewards_repository import RewardsRepository
from repositories.customers_repository import CustomersRepository

from rewardsservice.handlers.base_handler import NotFoundHandler

class App(tornado.web.Application):
    def __init__(self, db):
        self.logger = logging.getLogger(self.__class__.__name__)

        # Initialize the repositories as part of the tornado app
        self.rewards_repo = RewardsRepository(db)
        self.customers_repo = CustomersRepository(db)

        urls = build_url_patterns(self.rewards_repo, self.customers_repo)

        tornado.web.Application.__init__(self, urls, default_handler_class=NotFoundHandler, **settings)

# Move tornado app creation to the now async main to allow passing
# the mongo client
async def main():
    logger = logging.getLogger()
    tornado.options.parse_command_line()

    client = AsyncMongoClient("mongodb", settings["mongo_port"])
    # fail-fast with the mongo client before going further
    await client.admin.command("ping")
    db = client["Rewards"]
    logger.info("successful connection to mongo")

    app = App(db)
    
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    logger.info('Tornado server started on port {}'.format(options.port))

    # add in sigterm catching because the docker container
    # was taking a little bit to kill with each compose
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop_event.set)
    try:
        await stop_event.wait()
    finally:
        http_server.stop()
        await client.close()
        logger.info("Stopped server on port {}".format(options.port))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
