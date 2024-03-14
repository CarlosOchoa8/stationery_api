from app.api.routers import api_router
from fastapi import FastAPI

fastapi_app = FastAPI(
    title='stationery_api',
    description='stationery API',
    swagger_ui_parameters={'docExpansion': 'None'}
)

fastapi_app.include_router(
    router=api_router,
    prefix='/api/v1'
)

app = fastapi_app
