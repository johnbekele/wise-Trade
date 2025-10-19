from app.core.database import client
from beanie import Document ,PydanticObjectId
from typing import Type , List, TypeVar, Generic, Optional , Dict,Any
from pymongo.errors import DuplicateKeyError, OperationFailure

DocumentType = TypeVar("DocumentType", bound=Document)
class BaseRepository(Generic[DocumentType]):
    def __init__(self, model: Type[DocumentType]):
        self.model = model

    async def create(self, data: Dict[str, Any])-> DocumentType: 
        try:
            document = self.model(**data)
            await document.insert()
            return document
        except DuplicateKeyError as e:
            raise e
    
     # FindALL
    
    async def get_all(self,skip:int =0 ,limit:int =100)-> List[DocumentType]:
        return await self.model.find().skip(skip).limit(limit).to_list()
    
    async def get_by_id(self, id: str)-> Optional[DocumentType]:
        try:
            # Try using find_one with ObjectId
            document = await self.model.find_one({"_id": PydanticObjectId(id)})
            if document:
                return document
            return None
        except Exception as e:
            print(f"Error in get_by_id: {e}")
            return None
    
    async def find_one(self, query: dict)-> Optional[DocumentType]:
        return await self.model.find_one(query)
     # FindALL
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[DocumentType]:
        return await self.model.find_all().skip(skip).limit(limit).to_list()
    
    async def update(self, id: str, data: dict)-> Optional[DocumentType]:
        try:
            # Use find_one with PydanticObjectId for better compatibility
            document = await self.model.find_one({"_id": PydanticObjectId(id)})
            if document:
                for key, value in data.items():
                    setattr(document, key, value)
                await document.save()
            return document
        except Exception as e:
            print(f"Error in update method: {e}")
            return None
    
    async def delete(self, id: str)-> Optional[DocumentType]:
        document = await self.model.get(id)
        if document:
            await document.delete()
        return document
    
