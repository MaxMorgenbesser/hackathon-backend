from src.services.history import HistoryService

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/history")
def get_history():
    try:
        history_service = HistoryService()
        return history_service.get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))