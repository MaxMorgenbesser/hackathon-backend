from src.services.Base import BaseService


class TestBaseService:

    def test_supabase_client(self):
        base_service = BaseService()
        assert base_service.supabase_client() is not None

    def test_openai_client(self):
        base_service = BaseService()
        assert base_service.openai_client() is not None