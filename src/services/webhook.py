from fastapi import UploadFile
from src.services.Base import BaseService
from src.services.prompt import PromptService
import uuid
from datetime import datetime
import os


class WebhookService(BaseService):

    def __init__(self):
        super().__init__()
        self.prompt_service = PromptService()

    async def process_webhook(self, file: UploadFile, user_id: str = "123"):
        """Process uploaded file: check for spam and upload to storage"""
        try:
            import json
            
            # Check if the image is spam
            spam_result = await self.check_if_spam(file, user_id)
            spam_data = json.loads(spam_result)
            

            
            # Upload file to storage
            upload_result = await self.upload_file_to_storage(file)
            if spam_data:
                self.supabase_client().table("history").insert({
                   "user_id": "123",
                   "file": upload_result.get("public_url", ""),
                   "is_spam": spam_data.get("is_spam", False),
                }).execute()
            
            return { "is_spam": spam_data.get("is_spam")}
            
            
        except Exception as e:
            raise Exception(f"Webhook processing failed: {str(e)}")

    async def check_if_spam(self, file: UploadFile, user_id: str = "123"):
        """Check if an uploaded image contains spam mail content like coupons and unsolicited marketing"""
        try:
            # Fetch user prompt preferences
            user_prompt = self.prompt_service.get_prompt()
            
            # Check if OpenAI client is available
            openai_client = self.openai_client()
            if openai_client is None:
                raise Exception("OpenAI client not available - check OPENAI_API_KEY environment variable")
            
            # Convert image to base64 for OpenAI vision
            base64_image = await self.image_to_base64(file)
            
            # Determine content type based on filename
            content_type = "image/png" if file.filename.lower().endswith('.png') else "image/jpeg"
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "spam_detection",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "is_spam": {"type": "boolean"},
                                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                                "spam_type": {
                                    "type": "string",
                                    "enum": ["coupon", "unsolicited_marketing", "promotional", "junk_mail", "legitimate", "unknown"]
                                },
                                "reasoning": {"type": "string"},
                                "detected_elements": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["is_spam", "confidence", "spam_type", "reasoning", "detected_elements"]
                        }
                    }
                },
                messages=[
                    {
                        "role": "system",
                        "content": self._build_system_prompt(user_prompt)
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this image of mail and determine if it contains spam content. Look for coupons, marketing materials, promotional content, or unsolicited advertisements."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{content_type};base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Parse the response
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            raise Exception(f"Spam detection failed: {str(e)}")
    
    async def image_to_base64(self, file: UploadFile) -> str:
        """Convert uploaded image file to base64 string"""
        try:
            import base64
            
            # Read the file content
            file_content = await file.read()
            
            # Convert to base64
            base64_string = base64.b64encode(file_content).decode('utf-8')
            
            # Reset file pointer for potential reuse
            await file.seek(0)
            
            return base64_string
            
        except Exception as e:
            raise Exception(f"Failed to convert image to base64: {str(e)}")

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

    def _build_system_prompt(self, user_prompt):
        """Build a personalized system prompt based on user preferences"""
        base_prompt = (
            "You are a spam mail detection AI. Analyze images of mail/letters and determine if they contain spam content. "
            "Consider the user's specific preferences when making your determination.\n\n"
        )
        
        # Add user-specific preferences
        if user_prompt:
            preferences = []
            
            if not user_prompt.get('coupons', True):
                preferences.append("- DO NOT consider coupons and discount offers as spam (user wants to receive these)")
            else:
                preferences.append("- Consider coupons and discount offers as spam")
                
            if not user_prompt.get('Newsletters', True):
                preferences.append("- DO NOT consider newsletters as spam (user wants to receive these)")
            else:
                preferences.append("- Consider newsletters as spam")
                
            if not user_prompt.get('Feedback', True):
                preferences.append("- DO NOT consider feedback requests as spam (user wants to receive these)")
            else:
                preferences.append("- Consider feedback requests as spam")
            
            if user_prompt.get('exclusions'):
                exclusions = [exclusion.strip() for exclusion in user_prompt['exclusions'].split(',') if exclusion.strip()]
                if exclusions:
                    exclusions_text = ', '.join(exclusions)
                    preferences.append(f"- Additional exclusions: {exclusions_text}")
            
            if preferences:
                base_prompt += "USER PREFERENCES:\n" + "\n".join(preferences) + "\n\n"
        
        # Add general spam categories
        base_prompt += (
            "General spam categories include:\n"
            "- Unsolicited marketing materials\n"
            "- Promotional flyers\n"
            "- Junk mail advertisements\n"
            "- Credit card offers\n"
            "- Insurance solicitations\n"
            "- Political campaign materials\n"
            "- Charity solicitations\n\n"
            "Return a JSON response and only the json response and nothing else with:\n"
            "- is_spam: boolean indicating if the mail is spam\n"
            "- confidence: number between 0 and 1 indicating confidence level\n"
            "- spam_type: one of [coupon, unsolicited_marketing, promotional, junk_mail, legitimate, unknown]\n"
            "- reasoning: explanation of your decision\n"
            "- detected_elements: array of specific elements found in the image"
        )
        
        return base_prompt
