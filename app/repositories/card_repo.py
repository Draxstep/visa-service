from typing import Optional

import httpx

from app.core.settings import settings
from app.models.bank_schemas import ClienteBancarioPB


class CardRepository:
    def __init__(self) -> None:
        self._base_url = str(settings.POCKETBASE_URL).rstrip("/")

    async def obtener_tarjeta_por_numero(
        self, numero_tarjeta: str
    ) -> Optional[ClienteBancarioPB]:
        url = f"{self._base_url}/api/collections/clientes_bancarios/records"
        params = {"filter": f'numero_tarjeta="{numero_tarjeta}"'}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            payload = response.json()

        items = payload.get("items", [])
        if not items:
            return None

        return ClienteBancarioPB.model_validate(items[0])

    async def actualizar_saldo(self, id_registro: str, nuevo_saldo: float) -> None:
        url = f"{self._base_url}/api/collections/clientes_bancarios/records/{id_registro}"
        data = {"saldo": nuevo_saldo}

        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=data)
            response.raise_for_status()
