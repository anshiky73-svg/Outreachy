from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.repositories.influencer_repository import InfluencerRepository
from app.repositories.message_repository import MessageRepository
from app.services.ai.personalization_service import PersonalizationService

router = APIRouter(prefix="/api", tags=["Personalization"])


@router.post("/personalization/generate/{influencer_id}")
async def generate_message_for_influencer(influencer_id: str):
    influencer = InfluencerRepository().get(influencer_id)
    if influencer is None:
        raise HTTPException(status_code=404, detail="Influencer not found")
    message = await PersonalizationService().generate_for_influencer(influencer)
    return message


@router.post("/personalization/generate-bulk")
async def generate_bulk_messages():
    influencers = InfluencerRepository().list(limit=500)
    service = PersonalizationService()
    results = []
    for influencer in influencers:
        results.append(await service.generate_for_influencer(influencer))
    return {"count": len(results), "results": results}


@router.get("/personalization/{message_id}")
def get_message(message_id: str):
    message = MessageRepository().get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
