from app.core.database import client
from beanie import Document

class BaseRepository:
    def __init__(self, model: Document):
        self.model = model

    async def create(self, data: dict):
        document = self.model(**data)
        return await document.insert()
    
    async def get_all(self):
        return await self.model.find().to_list()
        