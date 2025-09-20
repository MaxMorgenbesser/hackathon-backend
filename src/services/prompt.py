from src.services.Base import BaseService
from src.models.prompt import Prompt


class PromptService(BaseService):

    def __init__(self):
        super().__init__()

    def update_prompt(self, prompt: Prompt):
     try:
        id = 123
        return self.supabase_client().table("promptSettings").update(prompt.model_dump()).eq("id", id).execute().data[0]
     except Exception as e:
        raise e


    def get_prompt(self):
        try:
            id = 123
            return self.supabase_client().table("promptSettings").select("*").eq("id", id).execute().data[0]

        except Exception as e:
            raise e