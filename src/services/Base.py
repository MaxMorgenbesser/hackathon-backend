from supabase import create_client, Client
import os

class BaseService:

    def supabase_client(self) -> Client:
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            return create_client(url, key)
        except Exception as e:
            print(e)
            return None