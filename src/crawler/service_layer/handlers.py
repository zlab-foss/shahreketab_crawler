import json
from typing import Callable, Dict, List, Type
from sqlalchemy import or_
from datetime import datetime

from src.crawler.adapters import orm, shahrekeetabonline
from src.crawler.domain import commands, events, model
from src.crawler.service_layer import unit_of_work
from src.crawler.service_layer.exceptions import *


def add_organization_info(
    cmd: commands.AddOrganization, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        organization = (
            uow.session.query(orm.organizations)
            .filter(
                or_(
                    orm.organizations.c.name == cmd.organization_name,
                    orm.organizations.c.email == cmd.email,
                )
            ).first()
        )
        if organization:
            raise DuplicateOrganizationInfo("Organization Name/Email Already Exists")

        new_org = model.Organization(
            name=cmd.organization_name,
            password=cmd.password,
            email=cmd.email,
            phone_number=cmd.phone_number,
            zipcode=cmd.zipcode,
            address=cmd.address,
            province=cmd.province,
            latitude=cmd.latitude,
            longitude=cmd.longitude
        )
        uow.session.add(new_org)
        uow.commit()



def crawl_product(
    cmd: commands.CrawlProduct,
    crawler: shahrekeetabonline.AbstractCrawler,
    uow: unit_of_work.AbstractUnitOfWork
):
    product = crawler.get_products(cmd.id,(cmd.id+1),1)
    with uow:
        product_obj = uow.products.get_by_product_id(int(product['products'][0]['id']))
        if product_obj:
            raise DuplicateProductID(f"The Product with id '{product['products'][0]['id']}' already exists")

        new_product = model.Product(
            id=product['products'][0]['id'],
            name=product['products'][0]['name'],
            description=product['products'][0]['description'],
            type_id=product['products'][0]['typeID'],
            available=product['products'][0]['available'],
            express_delivery=product['products'][0]['expressDelivery'],
            rating=product['products'][0]['averageRating'],
            attributes=list(map(lambda x: json.dumps(x), product['products'][0]['attributes']))
        )
        uow.products.add(new_product)
        uow.commit()
        
        write_log(
            event= events.ProductCrawled(product_id=product['products'][0]['id']) , uow=uow
        )



def write_log(
    event: events.ProductCrawled, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        new_log = model.Log(
            product_id=event.product_id,
            time_stamp=datetime.utcnow()
        )
        uow.session.add(new_log)
        uow.commit()



EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.ProductCrawled: [write_log]
}

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.AddOrganization: add_organization_info,
    commands.CrawlProduct: crawl_product,
}
