from beanie import Document, PydanticObjectId
from typing import Type, List, TypeVar, Generic, Optional, Dict, Any
from pymongo.errors import DuplicateKeyError, OperationFailure

DocumentType = TypeVar("DocumentType", bound=Document)
class BaseRepository(Generic[DocumentType]):
    def __init__(self, model: Type[DocumentType]):
        self.model = model
    
    def _convert_id(self, id: str) -> PydanticObjectId:
        """Convert string ID to PydanticObjectId - centralized conversion"""
        return PydanticObjectId(id)

    async def create(self, data: Dict[str, Any]) -> DocumentType:
        """Create a new document"""
        try:
            document = self.model(**data)
            await document.insert()
            return document
        except DuplicateKeyError as e:
            raise e
        except Exception as e:
            print(f"Error creating document: {e}")
            raise e
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[DocumentType]:
        """Find all documents with pagination"""
        try:
            return await self.model.find().skip(skip).limit(limit).to_list()
        except Exception as e:
            print(f"Error finding all documents: {e}")
            return []
    
    async def find_by_id(self, id: str) -> Optional[DocumentType]:
        """Find document by ID"""
        try:
            document = await self.model.find_one({"_id": self._convert_id(id)})
            return document
        except Exception as e:
            print(f"Error in find_by_id: {e}")
            return None
    
    async def get_by_id(self, id: str) -> Optional[DocumentType]:
        """Alias for find_by_id for backward compatibility"""
        return await self.find_by_id(id)
    
    async def find_one(self, query: dict) -> Optional[DocumentType]:
        """Find one document by query"""
        try:
            return await self.model.find_one(query)
        except Exception as e:
            print(f"Error in find_one: {e}")
            return None
    
    async def update(self, id: str, data: dict) -> Optional[DocumentType]:
        """Update document by ID"""
        try:
            document = await self.model.find_one({"_id": self._convert_id(id)})
            if document:
                for key, value in data.items():
                    setattr(document, key, value)
                await document.save()
            return document
        except Exception as e:
            print(f"Error in update method: {e}")
            return None
    
    async def delete(self, id: str) -> Optional[DocumentType]:
        """Delete document by ID"""
        try:
            document = await self.model.find_one({"_id": self._convert_id(id)})
            if document:
                await document.delete()
            return document
        except Exception as e:
            print(f"Error in delete method: {e}")
            return None
    
