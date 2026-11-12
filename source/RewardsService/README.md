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

---

# Implementation

## Quick start
```bash
cd source/RewardsService
docker-compose build
docker-compose up -d

# place an order, then read the rewards back
curl -X POST localhost:7050/orders -H "Content-Type: application/json" \
     -d '{"email": "customer01@gmail.com", "orderTotal": 100.80}'
curl localhost:7050/customers/customer01@gmail.com
curl localhost:7050/customers
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/orders` | **Endpoint 1**: submit an order; calculates, stores and returns the customer's rewards |
| `GET` | `/customers/{email}` | **Endpoint 2**: rewards data for one customer |
| `GET` | `/customers` | **Endpoint 3**: rewards data for all customers |
| `GET` | `/rewards` | The reward tiers (provided with the project) |

All responses are JSON. Every customer record has this shape:
```json
{
    "emailAddress": "customer01@gmail.com",
    "rewardPoints": 250,
    "rewardTier": "B",
    "rewardTierName": "10% off purchase",
    "nextRewardTier": "C",
    "nextRewardTierName": "15% off purchase",
    "nextRewardTierProgress": 0.5
}
```

### `POST /orders`
Request body:
```json
{ "email": "customer01@gmail.com", "orderTotal": 100.80 }
```
- Converts the order total to points (1 point per whole dollar, cents dropped), **adds them to the customer's existing points**, recalculates their tier and stores the result.
- Creates the customer on their first order, and updates the same record on later orders.
- Responds `201 Created` with the customer record.

| Status | When |
|---|---|
| `201` | Order accepted |
| `400` | Body isn't valid JSON or isn't a JSON object; `email` or `orderTotal` is missing; `email` isn't a non-empty string; `orderTotal` isn't a number, or is negative, `NaN` or `Infinity` |

### `GET /customers/{email}`
- Returns `200` with the customer record, or `404` if the customer has never placed an order.
- The email may be URL-encoded (`customer01%40gmail.com`) and is matched case-insensitively.

### `GET /customers`
- Returns `200` with a list of customer records, sorted by email.
- Returns `200` with `[]` when there are no customers yet.

### Errors
Every error response uses the same format:
```json
{ "error": "'orderTotal' must be a non-negative number" }
```
Unexpected server errors return `500` with `{"error": "Internal server error"}`. The details are written to the server log and never sent to the client.

## Design decisions

- **Points accumulate across orders and are capped at the top tier.** Two $150 orders give 300 points (tier C). Points stop at 1000 (tier J), because "once a customer has reached the top rewards tier, there are no more rewards the customer can earn."
- **Cents are dropped, not rounded**, so $100.80 earns 100 points. The conversion uses `Decimal` to avoid floating-point errors.
- **Progress is measured within the current tier band:**
  `(points − current tier threshold) / (next tier threshold − current tier threshold)`, rounded to 2 decimals.
  For example, 250 points is halfway from B (200) to C (300), giving `0.5`. The instructions' example (100 points at tier A with progress `0.5`) doesn't fit this or any other single formula, so I chose this one because it shows how far through the current tier the customer is. Progress is the fraction **completed**, from 0 to 1.
- **Below tier A and at tier J, missing values are `null`.** A customer with 50 points has `rewardTier: null`. A customer at tier J has `nextRewardTier`, `nextRewardTierName` and `nextRewardTierProgress` all set to `null`.
- **Tiers are read from the `rewards` collection, not hardcoded**, so MongoDB stays the single source of truth for tier thresholds and names.
- **Emails are trimmed and lowercased**, so `Customer01@Gmail.com` and `customer01@gmail.com` are the same customer.
- **Email format isn't validated.** Only a non-empty string is required. Full email validation is complex and still doesn't prove an address exists, so I left it out.
- **`orderTotal` must be a JSON number.** Numeric strings such as `"100"` and booleans are rejected rather than converted.
- **Async database access.** A single shared [Motor](https://motor.readthedocs.io/) client is created when the app starts and used by every handler. This avoids blocking Tornado's event loop and avoids opening a new connection on each request (the original `/rewards` handler did both).

## Project structure
```
rewardsservice/
├── app.py                  # Tornado app; creates the shared Motor client (self.db)
├── url_patterns.py         # routes → handlers
├── rewards_calculator.py   # pure functions: points_for_order, calculate_rewards
└── handlers/
    ├── base_handler.py       # BaseHandler: JSON error responses for all handlers
    ├── orders_handler.py     # POST /orders
    ├── customers_handler.py  # GET /customers, GET /customers/{email}
    └── rewards_handler.py    # GET /rewards
tests/
├── test_orders_endpoint.py     # calculator + POST /orders; defines FakeDatabase
├── test_customers_endpoint.py  # GET /customers/{email} and GET /customers
└── test_rewards_endpoint.py    # GET /rewards
```
The handlers only parse requests, call the calculator, read and write MongoDB, and build responses. The rewards logic itself is in `rewards_calculator.py`, which has no database or HTTP code, so it can be unit-tested on its own.

## Running the tests
```bash
cd source/RewardsService
docker-compose up -d
docker-compose exec rewardsservice python -m unittest discover -s tests -v
```
The tests run the real Tornado routes against an in-memory `FakeDatabase`, so they don't need or modify MongoDB data. They cover:
- the calculator's edge cases: 0, 50, 100, 250, 999, 1000 and 1500 points
- accumulating points and the top-tier cap
- email normalization
- every validation error
- JSON error responses
- `404` and empty-list behavior
- sorting
- making sure Mongo's `_id` is never returned

## Known limitations and possible improvements
- **Concurrent orders for the same customer can lose points.** The handler reads the customer's points, adds to them and writes them back. If two orders for one customer arrive at the same moment, one update can overwrite the other. The fix would be an atomic update (MongoDB `$inc`, combined with the cap).
- **No pagination on `GET /customers`.** It returns every customer in one response. With a large customer base it would need `limit`/`offset` parameters or cursor-based pagination.
- **No unique index on `emailAddress`.** The upsert keeps one record per customer, but a unique index would enforce this at the database level as well.
- **Unknown URLs** (e.g. `/foo`) return Tornado's default HTML 404 page rather than JSON.
- **MongoDB unavailable:** requests wait for the driver's default 30-second server-selection timeout before returning a `500`.
