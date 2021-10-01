from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

class Command:
    pass


@dataclass
class CrawlProduct(Command):
    id: UUID
    
