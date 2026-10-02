from __future__ import annotations

from fastapi import APIRouter

from app.services.discovery.discovery_service import DiscoveryService
from app.services.enrichment.enrichment_service import EnrichmentService
from app.services.filtering.filtering_service import FilteringService
from app.services.ai.personalization_service import PersonalizationService

router = APIRouter(prefix="/api", tags=["Pipeline"])


@router.post("/pipeline/run")
async def pipeline_run(payload: dict | None = None):
    payload = payload or {}
    run_discovery = payload.get("runDiscovery", True)
    run_filtering = payload.get("runFiltering", True)
    run_enrichment = payload.get("runEnrichment", True)
    run_personalization = payload.get("runPersonalization", True)

    results = {"runDiscovery": False, "runFiltering": False, "runEnrichment": False, "runPersonalization": False}

    if run_discovery:
        results["runDiscovery"] = True
        await DiscoveryService().run()
    if run_filtering:
        results["runFiltering"] = True
        FilteringService().run()
    if run_enrichment:
        results["runEnrichment"] = True
        await EnrichmentService().run()
    if run_personalization:
        results["runPersonalization"] = True
        influencers = []
        for influencer in __import__("app.repositories.influencer_repository", fromlist=["InfluencerRepository"]).InfluencerRepository().list(limit=500):
            if influencer.get("qualificationStatus") == "QUALIFIED":
                influencers.append(influencer)
        service = PersonalizationService()
        for influencer in influencers:
            await service.generate_for_influencer(influencer)

    return {"status": "completed", "stages": results}
