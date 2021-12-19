import inspect

from src.crawler.adapters import shahrekeetabonline, orm
from src.crawler.service_layer import messagebus, unit_of_work, handlers


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    crawler: shahrekeetabonline.AbstractCrawler = None,
) -> messagebus.MessageBus:

    if crawler is None:
        crawler = shahrekeetabonline.Crawler()

    if start_orm:
        orm.start_mapper()

    dependencies = {"uow": uow, "crawler": crawler}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }

    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        crawler=crawler,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
