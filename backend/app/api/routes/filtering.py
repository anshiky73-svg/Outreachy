from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.services.filtering.filtering_service import FilteringService

router = APIRouter(prefix="/api", tags=["Filtering"])


@router.post("/filtering/run")
def run_filtering():
    results = FilteringService().run()
    qualified = sum(1 for item in results if item["qualificationStatus"] == "QUALIFIED")
    failed = sum(1 for item in results if item["qualificationStatus"] == "FAILED")
    return {"summary": {"total": len(results), "qualified": qualified, "failed": failed}, "results": results}


@router.get("/filtering/results")
def filtering_results():
    return FilteringService().run()


@router.get("/influencers/{influencer_id}/qualification")
def qualification_route(influencer_id: str):
    influencer = FilteringService().influencer_repository.get(influencer_id)
    if influencer is None:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return {
        "influencerId": influencer_id,
        "qualificationStatus": influencer.get("qualificationStatus", "PENDING"),
        "qualificationReasons": influencer.get("qualificationReasons", []),
        "qualificationScore": influencer.get("qualificationScore", 0.0),
    }
