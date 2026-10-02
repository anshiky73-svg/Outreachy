from __future__ import annotations

from fastapi import APIRouter

from app.repositories.discovery_repository import DiscoveryRepository
from app.repositories.influencer_repository import InfluencerRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.outreach_repository import OutreachRepository

router = APIRouter(prefix="/api", tags=["Dashboard"])


@router.get("/dashboard/stats")
def dashboard_stats() -> dict:
    influencers = InfluencerRepository().list(limit=5000)
    discovery_runs = DiscoveryRepository().list()
    messages = MessageRepository().list()
    outreach_logs = OutreachRepository().list()

    total_influencers = len(influencers)
    qualified_influencers = sum(1 for item in influencers if item.get("qualificationStatus") == "QUALIFIED")
    failed_influencers = sum(1 for item in influencers if item.get("qualificationStatus") == "FAILED")
    emails_found = sum(1 for item in influencers if item.get("contactEmail") not in (None, "Not Found"))
    messages_generated = len(messages)
    emails_sent = sum(1 for item in outreach_logs if item.get("status") == "SENT")
    emails_simulated = sum(1 for item in outreach_logs if item.get("status") == "SIMULATED")
    failed_outreach = sum(1 for item in outreach_logs if item.get("status") == "FAILED")

    return {
        "totalInfluencers": total_influencers,
        "qualifiedInfluencers": qualified_influencers,
        "failedInfluencers": failed_influencers,
        "emailsFound": emails_found,
        "messagesGenerated": messages_generated,
        "emailsSent": emails_sent,
        "emailsSimulated": emails_simulated,
        "failedOutreach": failed_outreach,
        "recentDiscoveryRuns": discovery_runs[:5],
        "recentOutreach": outreach_logs[:5],
    }
