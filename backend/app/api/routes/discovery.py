from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.services.discovery.discovery_service import DiscoveryService

router = APIRouter(prefix="/api", tags=["Discovery"])


@router.post("/discovery/run")
async def run_discovery(
    niche: str = "Technology",
    queries: list[str] | None = None,
    candidate_limit: int = Query(default=150, ge=10, le=500),
):
    result = await DiscoveryService().run(niche=niche, queries=queries, candidate_limit=candidate_limit)
    return {"runId": result.get("_id"), "status": result.get("status"), "data": result}


@router.get("/discovery/runs")
def list_discovery_runs():
    from app.repositories.discovery_repository import DiscoveryRepository
    return DiscoveryRepository().list()


@router.get("/discovery/runs/{run_id}")
def get_discovery_run(run_id: str):
    from app.repositories.discovery_repository import DiscoveryRepository
    run = DiscoveryRepository().get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Discovery run not found")
    return run


@router.get("/discovery/runs/{run_id}/results")
def get_discovery_results(run_id: str):
    from app.repositories.discovery_repository import DiscoveryRepository
    from app.repositories.influencer_repository import InfluencerRepository
    repository = DiscoveryRepository()
    run = repository.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Discovery run not found")
    influencers = InfluencerRepository().list(limit=500)
    return {"runId": run_id, "influencers": influencers}
