import json	
import tornado.web	

from pymongo import MongoClient	
from tornado.gen import coroutine	
from tornado.options import options	

class CustomerHandler(tornado.web.RequestHandler):	
# GET Specific customer information	
    @coroutine	
    def get(self):	
        client = MongoClient(options.mongodb_host)	
        db = client["Customers"]	
        # email = "coco0@urbn.com"	
        email = self.get_argument("email", None)	
        if not email:	
            self.write("Email does not exist!")	
        else:	
            customers = list(db.customers.find({"email": email}, {"_id": 0}))	
            self.write(json.dumps(customers))	

# error handler	
    def write_error(self, status_code, **kwargs):	
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:	
            # in debug mode, try to send a traceback	
            self.set_header("Content-Type", "text/plain")	
            for line in traceback.format_exception(*kwargs["exc_info"]):	
                self.write(line)	
            self.finish()	
        else:	
            self.finish(	
                "<html><title>%(code)d: %(message)s</title>"	
                "<body>%(code)d: %(message)s</body></html>"	
                % {"code": status_code, "message": self._reason}	
            )