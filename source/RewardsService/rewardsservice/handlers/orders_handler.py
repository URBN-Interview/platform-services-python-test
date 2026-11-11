import json
import tornado.web
from rewards_calculator import points_for_order, calculate_rewards

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
        db = self.application.db
        tiers = await db.rewards.find({}, {"_id": 0}).to_list(None)

        points = points_for_order(order_total)
        result = calculate_rewards(points, tiers)
        result["emailAddress"] = email
        
        #4. Respond
        self.set_status(201)            #201 created
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))