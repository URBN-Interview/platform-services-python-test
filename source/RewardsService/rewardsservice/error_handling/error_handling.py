import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code in [403, 404, 500, 503]:
            self.write('Error %s' % status_code)
        else:
            self.write('Error. Please try again.')


class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    pass


class MainHandler(BaseHandler):
    def get(self):
        self.write('Error. Please try again.')