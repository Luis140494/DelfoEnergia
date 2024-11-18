from fastapi import APIRouter

from api.v1.endpoints import datafonte

api_router = APIRouter()

#api/v1/datas
api_router.include_router(datafonte.router, prefix='/data', tags=['datas'])
