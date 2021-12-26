from uuid import UUID
from datetime import datetime

from src.crawler.service_layer import unit_of_work, exceptions
from src.crawler.service_layer.exceptions import *



def get_product_by_id(
    product_id: str, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    try:
        with uow:
            product = uow.session.execute(
                """SELECT *
                    FROM product 
                    WHERE "id" = :product_id""",
                dict(product_id=str(product_id)),
            ).fetchone()
        return product
    except:
        raise exceptions.InvalidProduct("Invalid ProductID")


def get_last_log(
    uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        log = uow.session.execute(
            """SELECT *
                FROM log
                ORDER BY time_stamp DESC
                LIMIT 1
            """
        ).fetchone()
    
    if log:
        return log
    else:
        raise exceptions.InvalidLog("There is No Log to retrieve.")



def get_organization_by_id(
    organization_id: UUID, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        organization = uow.session.execute(
            """SELECT * 
                FROM organization
                WHERE "uuid" = :organization_id""",
            dict(organization_id=str(organization_id)),
        ).fetchone()
    return organization





def get_organization_by_email(
    organization_email: str, uow: unit_of_work.SqlAlchemyUnitOfWork
):
    with uow:
        organization = uow.session.execute(
            """SELECT * 
                FROM organization 
                WHERE "email" = :organization_email""",
            dict(organization_email=str(organization_email)),
        ).fetchone()
    return organization