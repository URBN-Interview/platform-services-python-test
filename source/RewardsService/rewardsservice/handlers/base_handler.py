# Shared base class for all API handlers. Its job is to make every error
# response JSON instead of Tornado's default HTML error page.

import json

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """Base class for API handlers: returns errors as JSON.

    Raise tornado.web.HTTPError(status, reason="message") in a handler and the
    client receives {"error": "message"} with that status code. Unexpected
    exceptions become a 500 with a generic message, so internal details
    (stack traces, database errors) are never sent to the client; Tornado
    still logs the full traceback on the server.
    """

    def write_error(self, status_code, **kwargs):
        if status_code >= 500:
            exc = kwargs.get("exc_info", (None, None, None))[1]
            # Only show messages we raised on purpose as HTTPError
            if isinstance(exc, tornado.web.HTTPError) and exc.reason:
                message = exc.reason
            else:
                message = "Internal server error"
        else:
            message = self._reason

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps({"error": message}))
