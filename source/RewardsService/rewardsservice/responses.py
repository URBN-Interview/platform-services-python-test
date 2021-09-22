import json


class JsonResponse:
    def __init__(self, code, status, message, extra_fields=None, errors=None):
        self.code = code
        self.status = status
        self.message = message
        self.extra_feilds = extra_fields
        self.errors = errors

    def response(self, handler):
        result = {
            "code": self.code,
            "status": self.status, 
            "message": self.message,
            "results": self.extra_feilds
        }
        if self.errors:
            result["errors"] = self.errors
        handler.write(json.dumps(result))
        handler.set_header("content-type", "application/json")