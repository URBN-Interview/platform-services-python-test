import json

import tornado.web

from pymongo.errors import PyMongoError

# Generic helper for API-related errors
class ApiError(tornado.web.HTTPError):
    def __init__(self, status_code, message):
        super().__init__(status_code)
        self.message = message

# Base handler for various helper functions that all child handlers can access

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    def write_json(self, data, status=200):
        self.set_status(status)
        self.finish(json.dumps(data))

    def write_error(self, status_code, **kwargs):
        e = kwargs.get("exc_info", (None, None, None))[1]
        if isinstance(e, ApiError):
            message=e.message
        elif isinstance(e, PyMongoError):
            status_code=503
            self.set_status(status_code)
            message = "mongo exception"
        elif status_code >= 500:
            message = "internal server error"
        else:
            message = self._reason
        self.finish(json.dumps({"error": {"status": status_code, "message": message}}))

class NotFoundHandler(BaseHandler):
    def prepare(self):
        raise ApiError(404, "resource not found")
