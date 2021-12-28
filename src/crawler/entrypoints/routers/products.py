from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from src.crawler import views
from src.crawler.config import Settings
from src.crawler.domain import commands
from src.crawler.entrypoints.models import products_schema
from src.crawler.service_layer import exceptions, messagebus


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key, algorithm = Settings().get_jwt_secrets()


def get_router(bus: messagebus.MessageBus):
    
    router = APIRouter(prefix="/product", tags=["Product"])

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def crawl_product(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required()
        authorize.get_jwt_subject()
        try:
            last_crawled_product = views.get_last_log(bus.uow)
            cmd = commands.CrawlProduct(
                id=(int(last_crawled_product.product_id)+1)
            )
            bus.handle(cmd)
            
        except exceptions.InvalidLog as e:
            cmd = commands.CrawlProduct(id=1)
            bus.handle(cmd)
        except exceptions.DuplicateProductID as e:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"{e}")



    @router.get("/{product_id}", status_code=status.HTTP_200_OK)
    async def get_product_by_id(
        product_id:int ,authorize: AuthJWT = Depends()
    ):
        try:
            authorize.jwt_required() 
            product = views.get_product_by_id(str(product_id), bus.uow)
            return product
        except exceptions.InvalidProduct as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")

    return router