"""Pure rewards calculation logic (no I/O), so it can be unit tested in isolation."""
import math
import re
from decimal import Decimal, InvalidOperation

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_EMAIL_LENGTH = 254


class ValidationError(ValueError):
    """Raised when client-supplied data is invalid."""


def normalize_email(email):
    """Validate an email address and return it trimmed and lower-cased."""
    if not isinstance(email, str):
        raise ValidationError("'email' must be a string")
    email = email.strip().lower()
    if not email or len(email) > MAX_EMAIL_LENGTH or not EMAIL_PATTERN.match(email):
        raise ValidationError("'email' must be a valid email address")
    return email


def parse_order_total(order_total):
    """Validate an order total and return it as a non-negative Decimal.

    Accepts numbers or numeric strings (e.g. 100.80 or "100.80"). Booleans are
    rejected even though they are ints in Python.
    """
    if isinstance(order_total, bool) or not isinstance(order_total, (int, float, str, Decimal)):
        raise ValidationError("'orderTotal' must be a number")
    try:
        total = Decimal(str(order_total).strip())
    except InvalidOperation:
        raise ValidationError("'orderTotal' must be a number")
    if not total.is_finite():
        raise ValidationError("'orderTotal' must be a finite number")
    if total < 0:
        raise ValidationError("'orderTotal' must not be negative")
    return total


def points_for_order(order_total):
    """One point per whole dollar spent, e.g. $100.80 earns 100 points."""
    return int(math.floor(parse_order_total(order_total)))


def sort_tiers(tiers):
    """Return the reward tiers ordered by the points required to reach them."""
    return sorted(tiers, key=lambda tier: tier["points"])


def max_points(tiers):
    """Points needed for the top tier; customers cannot earn beyond this."""
    return max((tier["points"] for tier in tiers), default=0)


def calculate_rewards(email, points, tiers):
    """Build a customer's rewards record from their accumulated points.

    * Points are capped at the top tier: once reached, no more rewards can be earned.
    * ``nextTierProgress`` is ``points / nextTier.points`` (100 points toward
      tier B at 200 points -> 0.5). At the top tier there is no next tier, so the
      next-tier fields are ``None`` and progress is ``1.0``.
    """
    ordered = sort_tiers(tiers)
    points = max(0, min(int(points), max_points(ordered)))

    current = None
    next_tier = None
    for tier in ordered:
        if points >= tier["points"]:
            current = tier
        else:
            next_tier = tier
            break

    if next_tier is None:
        progress = 1.0
    else:
        progress = round(points / next_tier["points"], 4)

    return {
        "email": email,
        "points": points,
        "tier": current["tier"] if current else None,
        "tierName": current["rewardName"] if current else None,
        "nextTier": next_tier["tier"] if next_tier else None,
        "nextTierName": next_tier["rewardName"] if next_tier else None,
        "nextTierProgress": progress,
    }
