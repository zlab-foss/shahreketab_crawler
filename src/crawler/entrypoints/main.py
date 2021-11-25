from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from src.crawler import bootstrap
from src.crawler.entrypoints.routers import (
    organization,
    product,
    log
)

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
app.include_router(product.get_router(bus))
app.include_router(log.get_router(bus))



@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
