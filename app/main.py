from app.api.routers import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI(
    title='stationery_api',
    description='stationery API',
    swagger_ui_parameters={'docExpansion': 'None'}
)

fastapi_app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(
    router=api_router,
    prefix='/api/v1'
)

app = fastapi_app
