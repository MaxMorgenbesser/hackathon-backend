from fastapi import UploadFile
from src.services.Base import BaseService
import uuid
from datetime import datetime
import os


class WebhookService(BaseService):

    def __init__(self):
        super().__init__()

    async def upload_file_to_storage(self, file: UploadFile):
        """Upload a file to Supabase storage"""
        try:
            # Generate unique filename to avoid conflicts
            file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # Read file content
            file_content = await file.read()
            
            # Upload to Supabase storage
            supabase = self.supabase_client()
            
            # Upload file to storage bucket (you'll need to create a bucket in Supabase)
            result = supabase.storage.from_("uploads").upload(
                path=unique_filename,
                file=file_content,
                file_options={
                    "content-type": file.content_type,
                    "cache-control": "3600"
                }
            )
            
            # Check if upload was successful
            if hasattr(result, 'error') and result.error:
                raise Exception(f"Upload failed: {result.error}")
            elif hasattr(result, 'data') and result.data is None:
                raise Exception("Upload failed: No data returned")
            
            # Get public URL for the uploaded file
            public_url = supabase.storage.from_("uploads").get_public_url(unique_filename)
            
            return {
                "filename": unique_filename,
                "original_filename": file.filename,
                "public_url": public_url,
                "bucket": "uploads",
                "uploaded_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def process_webhook(self, file: UploadFile):
        """Legacy method - kept for backward compatibility"""
        try:
            # This method can be used for additional processing if needed
            pass
        except Exception as e:
            raise e