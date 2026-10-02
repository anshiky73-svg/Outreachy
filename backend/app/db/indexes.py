from __future__ import annotations

from app.db.mongodb import get_database


def ensure_indexes() -> None:
    database = get_database()
    if database is None:
        return

    influencers = database["influencers"]
    discovery_runs = database["discovery_runs"]
    messages = database["messages"]
    outreach_logs = database["outreach_logs"]

    influencers.create_index([("platform", 1), ("platformId", 1)], unique=True)
    influencers.create_index([("contactEmail", 1)])
    influencers.create_index([("qualificationStatus", 1)])
    influencers.create_index([("niche", 1)])
    influencers.create_index([("followerCount", 1)])

    discovery_runs.create_index([("createdAt", -1)])
    discovery_runs.create_index([("status", 1)])

    messages.create_index([("influencerId", 1)])
    messages.create_index([("createdAt", -1)])

    outreach_logs.create_index([("influencerId", 1), ("channel", 1)])
    outreach_logs.create_index([("recipient", 1)])
    outreach_logs.create_index([("status", 1)])
    outreach_logs.create_index([("sentAt", -1)])
