from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

class Command:
    pass


@dataclass
class AddOrganization(Command):
    organization_name: str
    password: str
    email: Optional[str]
    phone_number: Optional[str]
    zipcode: Optional[str]
    address: Optional[str]
    province: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]



@dataclass
class CrawlProduct(Command):
    id: int
    
