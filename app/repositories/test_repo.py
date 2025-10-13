from .base_repository import BaseRepository
from app.models.users import User

class TestRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    async def get_all_users(self):
        return await self.get_all()
    
    async def create_user(self, user_data: dict):
        return await self.create(user_data)