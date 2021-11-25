from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.crawler.domain import events


class Product:
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        type_id: int = None,
        available: bool = True,
        express_delivery: bool = True,
        rating: Optional[float] = None,
        categories = List[str],
        attributes = List[str]
    ):
        self.name = name
        self.description = description
        self.type_id = type_id
        self.available = available
        self.express_delivery = express_delivery
        self.rating = rating
        self.categories = categories
        self.attributes = attributes
        self.events: List[events.Event] = []




@dataclass(unsafe_hash=True)
class Log:
    product_id: int
    time_stamp: datetime