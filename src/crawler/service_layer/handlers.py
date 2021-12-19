from typing import Callable, Dict, List, Type


from src.crawler import views
from src.crawler.adapters import orm
from src.crawler.domain import commands, events, model
from src.crawler.service_layer import unit_of_work
from src.crawler.service_layer.exceptions import *


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {}

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {}
