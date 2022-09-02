from lib2to3.pytree import Base
import tornado.web
from email_validator import validate_email, EmailNotValidError

class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code in [403, 404, 500, 503]:
            self.write('ERROR %s' % status_code)
        else:
            self.write('ERROR. Please try again.')


class MainHandler(BaseHandler):
    def get(self):
        self.write('ERROR. Please try again.')

class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    pass

class EmailErrorHandler():

      def validate_email_address(self, email):
        try:
            validation = validate_email(email)  
            email = validation["email"]
            return email
        except EmailNotValidError as exc:
            return [str(exc)]

            