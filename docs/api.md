# Visa Service API

## Base URL

- Local (default): http://localhost:8000
- API prefix: /api/v1

## Auth

- No authentication configured.

## Health Check

### GET /health

**Response 200**

```json
{
  "status": "ok"
}
```

## Autorizacion de tarjeta

### POST /api/v1/autorizar

Autoriza una transaccion para una tarjeta Visa registrada en PocketBase.

**Request body**

```json
{
  "numero_tarjeta": "string (12-19)",
  "cvc": "string (3-4)",
  "fecha_expiracion": "string (4-7)",
  "monto": 1000.0
}
```

**Validaciones**

- `numero_tarjeta`: longitud 12-19.
- `cvc`: longitud 3-4.
- `fecha_expiracion`: longitud 4-7.
- `monto`: debe ser mayor que 0.

**Response 200 (aprobado)**

```json
{
  "status": "aprobado",
  "mensaje": "Autorizacion aprobada",
  "codigo_autorizacion": "6b0700f7-6f2e-4c1b-9b84-3e9f91c6d4c3"
}
```

**Response 200 (rechazado)**

```json
{
  "status": "rechazado",
  "mensaje": "Fondos insuficientes",
  "codigo_autorizacion": null
}
```

**Posibles mensajes de rechazo**

- "Numero de tarjeta no corresponde a Visa"
- "Tarjeta no encontrada"
- "Franquicia no permitida"
- "Fondos insuficientes"

**Response 422 (validacion)**

Ejemplo de respuesta de validacion cuando `monto` <= 0.

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "monto"],
      "msg": "Value error, monto must be greater than 0",
      "input": 0
    }
  ]
}
```

**Response 500 (error interno)**

```json
{
  "detail": "Error interno al procesar la autorizacion"
}
```

## Dependencias externas

- **PocketBase**: se consulta la coleccion `clientes_bancarios` y se actualiza el `saldo`.

## Modelo esperado en PocketBase

Coleccion: `clientes_bancarios`

Campos requeridos:

```json
{
  "id": "string",
  "numero_tarjeta": "string",
  "cvc": "string",
  "franquicia": "string",
  "saldo": 1000.0
}
```

## Configuracion (.env)

Variables requeridas:

```
PROJECT_NAME=visa-service
POCKETBASE_URL=http://localhost:8090
FRANQUICIA_PERMITIDA=Visa
```

## Notas de negocio

- Se aprueba solo si el `numero_tarjeta` inicia con "4".
- Se rechaza si no existe el registro en PocketBase o la `franquicia` no coincide.
- El saldo se descuenta al aprobar y se actualiza en PocketBase.
