from uuid import UUID

import arrow
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from pydantic import BaseModel

from src.crawler import views
from src.crawler.config import Settings
from src.crawler.domain import commands
from src.crawler.entrypoints.models import organization_schemas
from src.crawler.service_layer import exceptions, messagebus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
secret_key, algorithm = Settings().get_jwt_secrets()


class Configs(BaseModel):
    authjwt_secret_key: str = secret_key
    authjwt_token_location: set = {"cookies"}
    # authjwt_cookie_secure: bool = True
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
    # authjwt_cookie_samesite: str = "none"
    authjwt_cookie_samesite: str = "lax"



def get_router(bus: messagebus.MessageBus):
    router = APIRouter(prefix="/organization", tags=["Organization"])

    @AuthJWT.load_config
    def get_config():
        return Configs()

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_organization(
        req: organization_schemas.OrganizationSignup
    ):
        try:
            cmd = commands.AddOrganization(
                req.name,
                pwd_context.hash(req.password),
                req.contact_info.email,
                req.contact_info.phone_number,
                req.geo_info.zipcode,
                req.geo_info.address,
                req.geo_info.province,
                req.location.latitude,
                req.location.longitude,
            )
            bus.handle(cmd)

        except exceptions.DuplicateOrganizationInfo as e:
            raise HTTPException(status.HTTP_409_CONFLICT, detail=f"{e}")


    @router.get("/me", status_code=status.HTTP_200_OK, response_model=organization_schemas.OrganizationGet)
    async def get_organization_by_id(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required()
        organization_id = authorize.get_jwt_subject()
        organization = views.get_organization_by_id(organization_id=UUID(organization_id), uow=bus.uow)
        return organization


    @router.post("/login", status_code=status.HTTP_200_OK)
    async def login_organization(
        org_data: organization_schemas.OrganizationSignin,
        authorize: AuthJWT = Depends(),
    ):
        try:
            organization = views.get_organization_by_email(
                organization_email=org_data.email, uow=bus.uow
            )

            if not organization:
                raise exceptions.InvalidOrganizationEmail("Organization Not Found")

            if not pwd_context.verify(org_data.password, organization.password):
                raise exceptions.IncorrectPassword("Password is Incorrect")

            if not organization.is_active:
                raise exceptions.InactiveOrganization("Organization is not Activate")

            access_token = authorize.create_access_token(
                subject=str(organization.uuid),
                expires_time=arrow.utcnow().shift(hours=1) - arrow.utcnow(),
                algorithm=algorithm,
            )

            refresh_token = authorize.create_refresh_token(
                subject=str(organization.uuid),
                expires_time=arrow.utcnow().shift(hours=24) - arrow.utcnow(),
                algorithm=algorithm,
            )

            authorize.set_access_cookies(access_token)
            authorize.set_refresh_cookies(refresh_token)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{e}")


    @router.post("/refresh", status_code=status.HTTP_200_OK)
    def refresh(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_refresh_token_required()
        current_organization_id = authorize.get_jwt_subject()
        new_access_token = authorize.create_access_token(
            subject=current_organization_id,
            expires_time=arrow.utcnow().shift(hours=1) - arrow.utcnow(),
            algorithm=algorithm,
        )
        authorize.set_access_cookies(new_access_token)


    @router.delete("/logout", status_code=status.HTTP_200_OK)
    def logout(
        authorize: AuthJWT = Depends()
    ):
        authorize.jwt_required()
        authorize.unset_jwt_cookies()

    return router


