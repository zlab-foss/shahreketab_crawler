from typing import Optional, List

from pydantic import BaseModel, EmailStr
from pydantic.schema import UUID

class Product(BaseModel):
    latitude: float
    longitude: float

