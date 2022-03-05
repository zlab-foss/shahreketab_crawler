from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.crawler import bootstrap
from src.crawler.entrypoints.routers import (
    organization,
    products,
    logs
)

from src.crawler.adapters import shahrekeetabonline
from src.crawler.domain import commands
from src.crawler import views
from src.crawler.service_layer import exceptions, handlers, unit_of_work

app = FastAPI()
bus = bootstrap.bootstrap()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organization.get_router(bus))
app.include_router(products.get_router(bus))
app.include_router(logs.get_router(bus))


# try:
#     last_crawled_product = views.get_last_log(uow=unit_of_work.SqlAlchemyUnitOfWork)
#     handlers.crawl_product(
#         cmd=commands.CrawlProduct(id=(int(last_crawled_product.product_id)+1)),
#         crawler=shahrekeetabonline.AbstractCrawler,
#         uow=unit_of_work.AbstractUnitOfWork
#     )
    
    
# except exceptions.InvalidLog as e:
#     cmd = commands.CrawlProduct(id=1)
#     handlers.crawl_product(
#         cmd = commands.CrawlProduct(id=1),
#         crawler=shahrekeetabonline.AbstractCrawler,
#         uow=unit_of_work.AbstractUnitOfWork
#     )


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
