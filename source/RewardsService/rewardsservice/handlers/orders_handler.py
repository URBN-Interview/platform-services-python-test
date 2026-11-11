import json
import tornado.web

class OrdersHandler(tornado.web.RequestHandler):

    async def post(self):
        #1. Read and parse the JSON body
        try:
            body = json.loads(self.request.body)
        except (json.JSONDecodeError, TypeError):
            raise tornado.web.HTTPError(400, reason="Request body must be valid JSON")

        #2. Pull out and validate the fields
        email = body.get("email")
        order_total = body.get("orderTotal")

        if not email or order_total is None:
            raise tornado.web.HTTPError(400, reason="'email' and 'orderTotal' are required")

        #3. Calculate and store customer rewards data into MongoDB

        result = {"email": email, "orderTotal": order_total}
        

        #4. Respond
        self.set_status(201)            #201 created
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))