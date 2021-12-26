from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from pydantic.schema import UUID

class Logs(BaseModel):
    id: UUID
    product_id: int
    time_stamp: datetime
    
    

