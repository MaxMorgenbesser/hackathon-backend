from src.services.webhook import WebhookService
from fastapi import UploadFile
import os
import traceback
import asyncio


class TestWebhookService:

    def test_process_webhook(self):
        try:
            webhook_service = WebhookService()

            # Get the absolute path to spam.jpg in the project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            spam_file_path = os.path.join(project_root, "spam.jpg")
            
            # Create UploadFile with file-like object
            file = UploadFile(filename="spam.jpg", file=open(spam_file_path, "rb"))
      
   
            # Run the async function
            result = asyncio.run(webhook_service.process_webhook(file))
            assert result is not None
            assert result.get("is_spam") is not None
            assert result.get("is_spam") is True
        except Exception as e:
            trace = traceback.format_exc()
            print(f"Trace: {trace}")       
            assert False