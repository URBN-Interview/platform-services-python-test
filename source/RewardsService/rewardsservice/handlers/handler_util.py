import math

# factored this out to make customer handler more readable


def processDocument(document, tierlist):
    update = {
        "tier": None,
        "rewardName": None,
        "nextTier": "A",
        "nextTierRewardName": "5% off purchase",
        "nextTierProgress": None
    }
    if document["points"] < 100:
        ###
        # See Engineering note 1 in log.md
        ###
        update["nextTierProgress"] = str(
            document["points"] - (math.floor(document["points"]/100)*100)) + "%"
    elif document["points"] < 1000:
        update["tier"] = tierlist[0]["tier"]
        update["rewardName"] = tierlist[0]["rewardName"]
        update["nextTier"] = tierlist[1]["tier"]
        update["nextTierRewardName"] = tierlist[1]["rewardName"]
        update["nextTierProgress"] = str(
            document["points"] - (math.floor(document["points"]/100)*100)) + "%"
    else:
        update["tier"] = "J"
        update["rewardName"] = "50% off purchase"
        update["nextTier"] = "Top Tier!!!"
        update["nextTierRewardName"] = "Top Tier!!!"
        update["nextTierProgress"] = "100%"

    return update
