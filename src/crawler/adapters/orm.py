import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    event,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import registry, relationship

from src.crawler.domain import model

mapper_registry = registry()


products = Table(
    "product",
    mapper_registry.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    ),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("type_id", Integer, nullable=False),
    Column("available", Boolean),
    Column("express_delivery", Boolean),
    Column("rating", Float),
    Column("categories", ARRAY(String)),
    Column("attributes", ARRAY(String))
)



logs = Table(
    "log",
    mapper_registry.metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    ),
    Column(
        "product_id",
        UUID(as_uuid=True),
        ForeignKey("product.id"),
        nullable=False,
    ),
    Column(
        "time_stamp",
        DateTime,
        default=datetime.utcnow()
    )
)


organizations = Table(
    "organization",
    mapper_registry.metadata,
    Column(
        "uuid",
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        unique=True,
        default=uuid.uuid4,
    ),
    Column("creation_time", DateTime, default=datetime.utcnow()),
    Column("name", String, unique=True, index=True),
    Column("password", String, nullable=False),
    Column("email", String, unique=True),
    Column("phone_number", String),
    Column("zipcode", String),
    Column("address", String),
    Column("province", String),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("is_active", Boolean, default=True),
    Column("is_deleted", Boolean, default=False),
)


def start_mapper():
    product_mapper = mapper_registry.map_imperatively(model.Product, products)
    
    log_mapper = mapper_registry.map_imperatively(
        model.Log,
        logs,
        properties={"product": relationship(product_mapper)}
    )




@event.listens_for(model.Product, "load")
def receive_load(product, _):
    product.events = []
