import json
import math

from tornado.web import HTTPError

from handlers.base_handler import BaseHandler
from rewards_calculator import points_for_order, calculate_rewards


class OrdersHandler(BaseHandler):

    async def post(self):
        # Read and parse the JSON body
        try:
            body = json.loads(self.request.body)
        except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
            raise HTTPError(400, reason="Request body must be valid JSON")

        # The body must be a JSON object, e.g. not a list or a bare number
        if not isinstance(body, dict):
            raise HTTPError(400, reason="Request body must be a JSON object")

        # Pull out and validate the fields
        email = body.get("email")
        order_total = body.get("orderTotal")

        if email is None or order_total is None:
            raise HTTPError(400, reason="'email' and 'orderTotal' are required")

        if not isinstance(email, str) or not email.strip():
            raise HTTPError(400, reason="'email' must be a non-empty string")

        # bool is a subclass of int in Python, so `true` would otherwise count as 1
        if isinstance(order_total, bool) or not isinstance(order_total, (int, float)):
            raise HTTPError(400, reason="'orderTotal' must be a number")

        # json.loads accepts NaN and Infinity, so reject those along with negatives
        if not math.isfinite(order_total) or order_total < 0:
            raise HTTPError(400, reason="'orderTotal' must be a non-negative number")

        # Normalize so "Customer01@Gmail.com" and "customer01@gmail.com" are the same customer
        email = email.strip().lower()

        db = self.application.db
        tiers = await db.rewards.find({}, {"_id": 0}).to_list(None)
        if not tiers:
            # The init_data seed job hasn't run - a server problem, not the client's fault
            raise HTTPError(500, reason="Reward tiers are not configured")

        # Add this order's points to any the customer already has
        customer = await db.customers.find_one({"emailAddress": email})
        existing_points = customer["rewardPoints"] if customer else 0
        total_points = existing_points + points_for_order(order_total)

        result = calculate_rewards(total_points, tiers)
        result["emailAddress"] = email

        # Create the customer document, or update it if it already exists
        await db.customers.update_one(
            {"emailAddress": email},     # which document
            {"$set": result},            # fields to write
            upsert=True,                 # insert it if no document matches
        )

        # Respond
        self.set_status(201)            # 201 Created
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(result))
