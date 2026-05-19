from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator


class AutorizacionRequest(BaseModel):
    numero_tarjeta: str = Field(min_length=12, max_length=19)
    cvc: str = Field(min_length=3, max_length=4)
    fecha_expiracion: str = Field(min_length=4, max_length=7)
    monto: float

    @field_validator("monto")
    @classmethod
    def validate_monto(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("monto must be greater than 0")
        return value


class AutorizacionResponse(BaseModel):
    status: Literal["aprobado", "rechazado"]
    mensaje: str
    codigo_autorizacion: Optional[str] = None


class ClienteBancarioPB(BaseModel):
    id: str
    numero_tarjeta: str
    cvc: str
    franquicia: str
    saldo: float
