# Objective
Create RESTful endpoint(s) to calculate, store, and retrieve customer rewards data from MongoDB.

# Background
* You will be using the [Tornado](http://www.tornadoweb.org) Python web framework and a MongoDB docker image.
* When starting up the 'rewardsservice' docker container in the [Setup](#setup) below, a mongo 'Rewards' database will be created for you with a "rewards" collection containing each reward a user can earn and how many points are needed to reach each reward.
    ```
    [
        { "tier": "A", "rewardName": "5% off purchase", "points": 100 },
        { "tier": "B", "rewardName": "10% off purchase", "points": 200 },
        { "tier": "C", "rewardName": "15% off purchase", "points": 300 },
        { "tier": "D", "rewardName": "20% off purchase", "points": 400 },
        { "tier": "E", "rewardName": "25% off purchase", "points": 500 },
        { "tier": "F", "rewardName": "30% off purchase", "points": 600 },
        { "tier": "G", "rewardName": "35% off purchase", "points": 700 },
        { "tier": "H", "rewardName": "40% off purchase", "points": 800 },
        { "tier": "I", "rewardName": "45% off purchase", "points": 900 },
        { "tier": "J", "rewardName": "50% off purchase", "points": 1000 }
    ]
    ```

# Instructions:
* Design and implement the following endpoints.
    * **Endpoint 1:**
        * Accept a customer's order data: **email adress**  (ex. "customer01@gmail.com") and **order total** (ex. 100.80).
        * Calculate and store the following customer rewards data into MongoDB. For each dollar a customer spends, the customer will earn 1 reward point. For example, an order of $100.80 earns 100 points. Once a customer has reached the top rewards tier, there are no more rewards the customer can earn.
            * **Email Address:** the customer's email address (ex. "customer01@gmail.com")
            * **Reward Points:** the customer's rewards points (ex. 100)
            * **Reward Tier:** the rewards tier the customer has reached (ex. "A")
            * **Reward Tier Name:** the name of the rewards tier (ex. "5% off purchase")
            * **Next Reward Tier:** the next rewards tier the customer can reach (ex. "B")
            * **Next Reward Tier Name:** the name of next rewards tier (ex. "10% off purchase")
            * **Next Reward Tier Progress:** the percentage the customer is away from reaching the next rewards tier (ex. 0.5)
    * **Endpoint 2:** Accept a customer's email address, and return the customer's rewards data that was stored in Endpoint 1.
    * **Endpoint 3:** Return the same rewards data as Endpoint 2 but for all customers.
* Add error handling and unit tests.

# Setup
* Install docker and docker-compose dependencies.
* $ cd APP_PATH/platform-services-python-test/source/RewardsService
* $ docker-compose build
* $ docker-compose up -d
* Services are accessible at http://localhost:7050/

# API

All responses are JSON. Errors use the shape `{"error": {"code": <status>, "message": "<details>"}}`.

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| `GET` | `/rewards` | List reward tiers | `200` | `503` |
| `POST` | `/orders` | **Endpoint 1** – record an order and store the customer's recalculated rewards | `201` + `Location` header | `400`, `503` |
| `GET` | `/customers/{email}` | **Endpoint 2** – one customer's rewards (email may be URL-encoded) | `200` | `400`, `404`, `503` |
| `GET` | `/customers` | **Endpoint 3** – rewards for all customers | `200` | `503` |

### Examples
```
$ curl -X POST http://localhost:7050/orders -d '{"email": "customer01@gmail.com", "orderTotal": 100.80}'
{"email": "customer01@gmail.com", "points": 100, "tier": "A", "tierName": "5% off purchase",
 "nextTier": "B", "nextTierName": "10% off purchase", "nextTierProgress": 0.5}

$ curl http://localhost:7050/customers/customer01@gmail.com
$ curl http://localhost:7050/customers
```

### Rewards rules
* 1 point per whole dollar per order (`$100.80` → 100 points). Points accumulate across orders.
* Emails are trimmed and lower-cased, so `Customer01@Gmail.com` and `customer01@gmail.com` are the same customer.
* Points are capped at the top tier (1000); once a customer reaches tier J they earn no more rewards.
* `nextTierProgress` = `points / nextTier.points` (e.g. 100 of 200 → `0.5`). Customers below tier A have
  `tier`/`tierName` of `null`. At the top tier, `nextTier`/`nextTierName` are `null` and progress is `1.0`.
* Point updates are atomic in MongoDB, so concurrent orders for the same customer are never lost.

# Running the tests
```
$ docker-compose run --rm rewardsservice sh -c "cd rewardsservice && python -m unittest discover -s tests -t ."
```
