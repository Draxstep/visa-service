import uuid

from app.core.settings import settings
from app.models.bank_schemas import AutorizacionRequest, AutorizacionResponse
from app.repositories.card_repo import CardRepository


class BankService:
    def __init__(self, card_repository: CardRepository) -> None:
        self._card_repository = card_repository

    async def procesar_autorizacion(
        self, datos: AutorizacionRequest
    ) -> AutorizacionResponse:
        if not datos.numero_tarjeta.startswith("4"):
            return AutorizacionResponse(
                status="rechazado",
                mensaje="Numero de tarjeta no corresponde a Visa",
            )

        tarjeta = await self._card_repository.obtener_tarjeta_por_numero(
            datos.numero_tarjeta
        )
        if tarjeta is None:
            return AutorizacionResponse(
                status="rechazado",
                mensaje="Tarjeta no encontrada",
            )

        if tarjeta.franquicia != settings.FRANQUICIA_PERMITIDA:
            return AutorizacionResponse(
                status="rechazado",
                mensaje="Franquicia no permitida",
            )

        if datos.monto > tarjeta.saldo:
            return AutorizacionResponse(
                status="rechazado",
                mensaje="Fondos insuficientes",
            )

        nuevo_saldo = tarjeta.saldo - datos.monto
        await self._card_repository.actualizar_saldo(tarjeta.id, nuevo_saldo)

        return AutorizacionResponse(
            status="aprobado",
            mensaje="Autorizacion aprobada",
            codigo_autorizacion=str(uuid.uuid4()),
        )
