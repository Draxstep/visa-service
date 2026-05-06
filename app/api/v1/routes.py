from fastapi import APIRouter

from app.controllers.auth_controller import autorizar_tarjeta
from app.models.bank_schemas import AutorizacionRequest, AutorizacionResponse

router = APIRouter()


@router.post("/autorizar", response_model=AutorizacionResponse)
async def autorizar(datos: AutorizacionRequest) -> AutorizacionResponse:
    return await autorizar_tarjeta(datos)
