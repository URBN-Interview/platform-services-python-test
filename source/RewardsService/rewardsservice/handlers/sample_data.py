# GET /customers with input JSON object
customerGet = {
    "email": "mickannese@gmail.com"
}

# response object
customerResponse = {
    "nextTierRewardName": "20% off purchase",
    "email": "mickannese@gmail.com",
    "rewardName": "15% off purchase",
    "tier": "C",
    "points": 396,
    "nextTier": "D",
    "nextTierProgress": "96%"
}

# POST /customers with input JSON object:
customerPost = {
    "email": "mickannese@gmail.com",
    "cost": 155.78
}

# response string with updated points
ThankYouString = "Thank you for your purchase mickannese@gmail.com!!!!! Your new point total is 551 points!!!"


# GET /admin response array of objects:


# response array of objects:

adminResponse = [
    {
        "tier": "C",
        "email": "mickannese@gmail.com",
        "nextTierRewardName": "20% off purchase",
        "nextTier": "D",
        "points": 396,
        "nextTierProgress": "96%",
        "rewardName": "15% off purchase"
    },
    {
        "tier": "C",
        "email": "mick42895@gmail.com",
        "nextTierRewardName": "20% off purchase",
        "nextTier": "D",
        "points": 341,
        "nextTierProgress": "41%",
        "rewardName": "15% off purchase"
    }]
