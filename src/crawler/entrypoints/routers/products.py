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
    async def create_industry(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required()
        organization_id = authorize.get_jwt_subject()
        try:
            pass
        except (exceptions.DuplicateIndustry) as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{e}")



    @router.get("/{industry_id}", status_code=status.HTTP_200_OK, response_model=products_schema.Product)
    async def get_industry_by_id(
        industry_id:UUID ,authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required() 
        industry = views.get_industry_by_id(str(industry_id), bus.uow)
        return industry

    return router