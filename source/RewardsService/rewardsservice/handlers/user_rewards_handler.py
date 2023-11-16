import tornado.web
import json

from tornado.gen import coroutine
from bson import json_util
from .rewards_base_handler import RewardsBaseHandler


class GetUserRewardsHandler(RewardsBaseHandler):
    """
    GetUserRewardsHandler is responsible for collecting the
    requested User rewards information. If no user is supplied
    to the handler, all rewards details will be returned.
    This handler inherits the mongo client, db and logger
    from RewardsBaseHandler
    """

    @coroutine
    def get(self):
        """
        GET request expecting a 'customerEmail' query parameter.
        However, upon lack of supplied param, the handler
        simply returns the user rewards information for
        all users in the users collection
        """

        customer_email = self.get_query_argument("customerEmail", None)
        if customer_email:
            is_valid, err = self.validate_email(customer_email)
            if not is_valid:
                self.logger.warn(err)
                raise tornado.web.HTTPError(400, reason=err)

            user = self.db.users.find_one({"email": customer_email})
            if not user:
                response = {"err": "User not found"}
                self.logger.warn(response)
                raise tornado.web.HTTPError(404, reason=response["err"])

            else:
                response = {"user": user}
                self.write(json_util.dumps(response))

        else:
            all_users = [docs for docs in self.db.users.find({})]
            response = {"allUsers": all_users}
            self.write(json_util.dumps(response))
