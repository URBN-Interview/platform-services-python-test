from http import HTTPStatus

import tornado.web
from pymongo import MongoClient, errors
from tornado.escape import json_decode
from tornado.gen import coroutine

DB_TIMEOUT_SEC = 3


class MongoMixin(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(MongoMixin, self).__init__(*args, **kwargs)
        self.client = MongoClient("mongodb", 27017, serverSelectionTimeoutMS=DB_TIMEOUT_SEC*1000)
        self.db = self.client["Rewards"]

    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.clear()
        self.set_status(status_code)
        _, error, _ = kwargs.get('exc_info')
        if hasattr(error, 'reason'):
            reason = error.reason or 'Unknown error'
        else:
            reason = str(error)
        self.finish({'code': status_code, 'message': reason})

    @staticmethod
    def decode_body(func):
        def wrapper(*args, **kwargs):
            if not args[0].request.body:
                raise tornado.web.HTTPError(400, reason='No body in request')
            setattr(args[0].request, 'decoded_body', json_decode(args[0].request.body))
            func(*args, **kwargs)
        return wrapper


class RootHandler(MongoMixin):

    @coroutine
    def get(self):
        # verifies database connection
        try:
            server_info = self.client.server_info()
            response = {'status': 0, 'message': 'OK', 'details': server_info}
            self.write(response)
        except errors.ServerSelectionTimeoutError:
            self.write_error(HTTPStatus.SERVICE_UNAVAILABLE)
