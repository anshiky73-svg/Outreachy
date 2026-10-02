from fastapi import APIRouter

from app.db.mongodb import check_database_connection


router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    database_connected = check_database_connection()
    return {
        "status": "ok" if database_connected else "degraded",
        "database": "connected" if database_connected else "disconnected",
    }