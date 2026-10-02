from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.repositories.influencer_repository import InfluencerRepository

router = APIRouter(prefix="/api", tags=["Influencers"])


@router.get("/influencers")
def list_influencers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    platform: str | None = None,
    niche: str | None = None,
    status: str | None = None,
):
    repo = InfluencerRepository()
    items = repo.list(skip=skip, limit=limit, platform=platform, niche=niche, status=status)
    return {"items": items, "count": len(items), "skip": skip, "limit": limit}


@router.get("/influencers/{influencer_id}")
def get_influencer(influencer_id: str):
    influencer = InfluencerRepository().get(influencer_id)
    if influencer is None:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return influencer


@router.get("/influencers/{influencer_id}/qualification")
def get_qualification(influencer_id: str):
    influencer = InfluencerRepository().get(influencer_id)
    if influencer is None:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return {
        "influencerId": influencer_id,
        "qualificationStatus": influencer.get("qualificationStatus", "PENDING"),
        "qualificationReasons": influencer.get("qualificationReasons", []),
        "qualificationScore": influencer.get("qualificationScore", 0.0),
    }


@router.get("/influencers/export")
def export_influencers():
    rows = InfluencerRepository().export_rows()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Platform", "Followers", "Engagement", "Niche", "Email", "Profile URL", "Content Themes", "Status"])
    for item in rows:
        writer.writerow([
            item.get("name", "Not Found"),
            item.get("platform", "Not Found"),
            item.get("followerCount", 0),
            item.get("engagementRate", 0),
            item.get("niche", "Not Found"),
            item.get("contactEmail", "Not Found"),
            item.get("profileUrl", "Not Found"),
            "; ".join(item.get("contentThemes") or []),
            item.get("qualificationStatus", "PENDING"),
        ])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=influencers.csv"})
