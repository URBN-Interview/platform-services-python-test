import json
import logging

import tornado.web
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


class BaseHandler(tornado.web.RequestHandler):
    """Common JSON request/response and error handling for API handlers."""

    def initialize(self, repository):
        self.repository = repository

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def write_json(self, data, status=200):
        self.set_status(status)
        self.finish(json.dumps(data))

    def read_json_body(self):
        try:
            body = json.loads(self.request.body or b"")
        except ValueError:
            raise tornado.web.HTTPError(400, reason="Request body must be valid JSON")
        if not isinstance(body, dict):
            raise tornado.web.HTTPError(400, reason="Request body must be a JSON object")
        return body

    def write_error(self, status_code, **kwargs):
        message = self._reason
        exc_info = kwargs.get("exc_info")
        if exc_info and isinstance(exc_info[1], PyMongoError):
            status_code = 503
            self.set_status(status_code)
            message = "Rewards database is unavailable, please try again later"
        elif exc_info and not isinstance(exc_info[1], tornado.web.HTTPError):
            message = "Internal server error"
        self.finish(json.dumps({"error": {"code": status_code, "message": message}}))
