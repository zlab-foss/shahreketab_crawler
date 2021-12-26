from typing import Optional, List

from pydantic import BaseModel, EmailStr
from pydantic.schema import UUID

class Product(BaseModel):
    name: str
    description: str
    type_id: int
    available: bool
    express_delivery: bool
    rating: Optional[float]
    attributes: List[str]
    

