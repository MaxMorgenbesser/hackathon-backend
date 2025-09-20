from src.services.Base import BaseService   

class HistoryService(BaseService):
    def __init__(self):
        super().__init__()

    def get_history(self, ):
        try:
            return self.supabase_client().table("history").select("*").eq("user_id", 123).execute()
        except Exception as e:
            raise e
