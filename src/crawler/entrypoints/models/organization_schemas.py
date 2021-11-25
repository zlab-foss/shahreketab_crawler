from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic.schema import UUID


class Location(BaseModel):
    latitude: float
    longitude: float


class GeoInfo(BaseModel):
    address: Optional[str] = ""
    province: Optional[str] = ""
    zipcode: Optional[str] = ""


class OrganizationContactInfo(BaseModel):
    phone_number: Optional[str] = ""
    email: EmailStr


class OrganizationBase(BaseModel):
    name: str
    contact_info: OrganizationContactInfo
    geo_info: GeoInfo
    location: Location


class OrganizationSignin(BaseModel):
    email: EmailStr
    password: str


class OrganizationSignup(OrganizationBase):
    password: str


class Organization(OrganizationBase):
    id: UUID
    is_active: bool
    is_deleted: bool



