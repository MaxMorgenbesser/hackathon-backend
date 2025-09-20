from fastapi import APIRouter, HTTPException
from src.models.prompt import Prompt
from src.services.prompt import PromptService

router = APIRouter()

@router.put("/prompt")
def update_prompt(prompt: Prompt):
  try:
    prompt_service = PromptService()
    return prompt_service.update_prompt(prompt)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@router.get("/prompt")
def get_prompt():
  try:
    prompt_service = PromptService()
    return prompt_service.get_prompt()
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))