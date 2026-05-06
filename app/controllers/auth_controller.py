from fastapi import HTTPException

from app.models.bank_schemas import AutorizacionRequest, AutorizacionResponse
from app.repositories.card_repo import CardRepository
from app.services.bank_service import BankService


async def autorizar_tarjeta(
    datos: AutorizacionRequest,
) -> AutorizacionResponse:
    try:
        repository = CardRepository()
        service = BankService(repository)
        return await service.procesar_autorizacion(datos)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail="Error interno al procesar la autorizacion"
        ) from exc
