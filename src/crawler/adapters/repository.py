import abc
from typing import Set

from src.crawler.adapters import orm
from src.crawler.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: Set[model.Product] = set()

    def add(self, product: model.Product):
        self._add(product)
        self.seen.add(product)

    def get_by_product_id(self, product_id) -> model.Product:
        product = self._get_by_product_id(product_id)
        if product:
            self.seen.add(product)
        return product


    @abc.abstractmethod
    def _add(self, product: model.Product):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_product_id(self, product_id) -> model.Product:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, product):
        self.session.add(product)

    def _get_by_product_id(self, product_id):
        return (
            self.session.query(model.Product)
            .filter(orm.products.c.id == product_id)
            .first()
        )
