from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.crawler.domain import events


class Product:
    def __init__(
        self,
        id: int,
        name: str,
        description: Optional[str] = None,
        type_id: int = None,
        available: bool = True,
        express_delivery: bool = True,
        rating: Optional[float] = None,
        attributes = List[str]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type_id = type_id
        self.available = available
        self.express_delivery = express_delivery
        self.rating = rating
        self.attributes = attributes
        self.events: List[events.Event] = []


@dataclass(unsafe_hash=True)
class Organization:
    name: str
    password: str
    email: str
    phone_number: Optional[str] = None
    zipcode: Optional[str] = None
    address: Optional[str] = None
    province: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass(unsafe_hash=True)
class Log:
    product_id: int
    time_stamp: datetime