import math

def updateCustomerPoints(db, email, totalpoints):
    db.customers.update({'email':email},{"$set":{'rewardpoints':totalpoints}})

def calculateTotalPoints(db, orderTotal, email):
    # Splits the string and returns the whole number then converts the number to an int
    pointsString = orderTotal.split('.')[0]
    newPoints = int(pointsString)

    # Retrieves the customer data and gets the current total points for the customer
    # Adds the new points with the current points
    customer = list(db.customers.find({"email":email}, {"_id": 0}))
    customerCurrentPoints = customer[0]["rewardpoints"]
    totalpoints = customerCurrentPoints + newPoints
    return totalpoints

def calculateCurrentPointsTier(db, totalpoints):
    pointsTier = int(math.floor(totalpoints / 100.0)) * 100
    if(pointsTier < 100):
        return None
    if(pointsTier > 1000):
        pointsTier = 1000
    customerPointsTier = list(db.rewards.find({"points":pointsTier}, {"_id": 0}))
    return customerPointsTier[0]["rewardName"]

def calculateCurrentRewardTierName(db, totalpoints):
    pointsTier = int(math.floor(totalpoints / 100.0)) * 100
    if(pointsTier < 100):
        return None
    if(pointsTier > 1000):
        pointsTier = 1000

    customerPointsTier = list(db.rewards.find({"points":pointsTier}, {"_id": 0}))
    return customerPointsTier[0]["tier"]

def calculateNextPointsTier(db, totalpoints):
    pointsTier = int(math.ceil(totalpoints / 100.0)) * 100
    if(pointsTier > 1000):
        pointsTier = 1000
    if(pointsTier < 100):
        pointsTier = 100
    customerPointsTier = list(db.rewards.find({"points":pointsTier}, {"_id": 0}))
    return customerPointsTier[0]["rewardName"]

def calculateNextRewardTierName(db, totalpoints):
    pointsTier = int(math.ceil(totalpoints / 100.0)) * 100
    if(pointsTier > 1000):
        pointsTier = 1000
    if(pointsTier < 100):
        pointsTier = 100
    customerPointsTier = list(db.rewards.find({"points":pointsTier}, {"_id": 0}))
    return customerPointsTier[0]["tier"]

def calculateNextRewardTierProgress(db, totalpoints):
    pointsTier = int(math.ceil(totalpoints / 100.0)) * 100
    if(pointsTier > 1000):
        return 0
    if(pointsTier < 100):
        pointsTier = 100
    customerPointsTier = list(db.rewards.find({"points":pointsTier}, {"_id": 0}))
    return ((customerPointsTier[0]["points"] - totalpoints) * 0.01)

def composeCustomerData(email, rewardpoints, rewardtier, rewardtiername, nextrewardtier, nextrewardtiername,  nextrewardtierprogress):
    customerData = {
            "EmailAddress": email,
            "RewardPoints": rewardpoints,
            "RewardTier": rewardtier,
            "RewardTierName": rewardtiername,
            "NextRewardTier": nextrewardtier,
            "NextRewardTierName": nextrewardtiername,
            "NextRewardTierProgress":nextrewardtierprogress,
        }
    return customerData