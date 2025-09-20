
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.webhook import WebhookService
router = APIRouter()


@router.post("/webhook")
async def process_file_upload(file: UploadFile = File(...)):
    """Upload a file, detect spam content, and save to Supabase storage"""
    try:
        print(f"Route received file: {file}")
        print(f"File type: {type(file)}")
       
        
        webhook_service = WebhookService()
        result = await webhook_service.process_webhook(file)
        print(f"Result: {result}")
        return result

    except Exception as e:
        print(f"Error in route: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


