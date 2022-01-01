from dataclasses import dataclass
from typing import  Optional

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
    

@dataclass
class DeleteProduct(Command):
    organization_id: str
    product_id: str