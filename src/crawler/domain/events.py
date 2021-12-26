from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

class Event:
    pass


@dataclass
class ProductCrawled(Event):
    product_id: int
    