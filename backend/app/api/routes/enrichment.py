from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.services.enrichment.enrichment_service import EnrichmentService

router = APIRouter(prefix="/api", tags=["Enrichment"])


@router.post("/enrichment/run")
async def run_enrichment():
    result = await EnrichmentService().run()
    return {"status": "completed", "results": result}


@router.post("/enrichment/{influencer_id}")
async def enrich_single_influencer(influencer_id: str):
    try:
        return await EnrichmentService().enrich_influencer(influencer_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
