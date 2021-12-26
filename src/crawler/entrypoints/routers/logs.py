from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext

from src.crawler import views
from src.crawler.config import Settings
from src.crawler.entrypoints.models import logs_schema
from src.crawler.service_layer import exceptions, messagebus


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key, algorithm = Settings().get_jwt_secrets()


def get_router(bus: messagebus.MessageBus):
    
    router = APIRouter(prefix="/log", tags=["Log"])

    @router.get("/", status_code=status.HTTP_200_OK, response_model=logs_schema.Logs)
    async def get_last_log(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required()
        try: 
            log = views.get_last_log(bus.uow)
            return log
        except exceptions.InvalidLog as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")

    return router