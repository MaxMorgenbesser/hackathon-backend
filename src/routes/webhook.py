
from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.webhook import WebhookService

router = APIRouter()


@router.post("/webhook")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to Supabase storage"""
    webhook_service = WebhookService()
    
    try:
        result = await webhook_service.upload_file_to_storage(file)
        return {
            "message": "File uploaded successfully",
            "file_info": {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size
            },
            "storage_info": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/webhook")
def get_webhook():
    return {"message": "Hello World"}