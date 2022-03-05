import json
import time
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
    c = crawler()
    product = c.get_products(
        from_id=cmd.id,
        to_id=(cmd.id+1),
        page=1)

    if product['products']:
        if product['products'][0]['name']:
            with uow:
                product_obj = uow.products.get_by_product_id(int(product['products'][0]['id']))
                if product_obj:
                    raise DuplicateProductID(f"The Product with id '{product['products'][0]['id']}' already exists")

                if 'description' in product['products'][0]:
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
                else:
                    new_product = model.Product(
                        id=product['products'][0]['id'],
                        name=product['products'][0]['name'],
                        description=None,
                        type_id=product['products'][0]['typeID'],
                        available=product['products'][0]['available'],
                        express_delivery=product['products'][0]['expressDelivery'],
                        rating=product['products'][0]['averageRating'],
                        attributes=list(map(lambda x: json.dumps(x), product['products'][0]['attributes']))
                    )
                uow.products.add(new_product)
                uow.commit()
                print(f"product with id = {cmd.id} just crawled.")
                
                write_log(
                    event= events.ProductCrawled(product_id=product['products'][0]['id']),
                    crawler=crawler,
                    uow=uow
                )
        else:
            crawl_product(
                cmd=commands.CrawlProduct(id=(cmd.id + 1)),
                crawler=crawler,
                uow=uow
                )
    else:
        crawl_product(
            cmd=commands.CrawlProduct(id=(cmd.id + 1)),
            crawler=crawler,
            uow=uow
        )


def delete_product(
    cmd: commands.DeleteProduct, uow: unit_of_work.AbstractUnitOfWork
):
    with uow:
        delete_log(
            event=events.ProductDeleted(product_id=int(cmd.product_id)),
            uow=uow
        )

        product_obj = uow.products.get_by_product_id(int(cmd.product_id))
        if not product_obj:
            raise InvalidProduct("Invalid ProductID")
        
        uow.products.delete_by_product_id(product_id=product_obj.id)
        uow.commit()


def write_log(
    event: events.ProductCrawled,
    crawler: shahrekeetabonline.AbstractCrawler,
    uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        new_log = model.Log(
            product_id=event.product_id,
            time_stamp=datetime.utcnow()
        )
        uow.session.add(new_log)
        uow.commit()
        
        time.sleep(1)
        
        crawl_product(
            cmd=commands.CrawlProduct(id=(event.product_id + 1)),
            crawler=crawler,
            uow=uow
        )


def delete_log(
    event: events.ProductDeleted, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        log_obj = (
            uow.session.query(orm.logs)
            .filter(orm.logs.c.product_id == event.product_id)
            .first()
        )
        if not log_obj:
            pass
        
        uow.session.query(orm.logs).filter(
            orm.logs.c.product_id == event.product_id
        ).delete()
        uow.commit()




EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.ProductCrawled: [write_log],
    events.ProductDeleted: [delete_log],
}

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.AddOrganization: add_organization_info,
    commands.CrawlProduct: crawl_product,
    commands.DeleteProduct: delete_product,
}
