from pydantic import BaseModel, validator, Field
from typing import Optional
import sys
import os

# Añadir el directorio raíz al path para importar utils y base_schemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validators import *
from schemas.base_schemas import ServicioPermanenciaBase

class POPSBase(BaseModel):
    """Esquema base para validación de datos POPS."""
    id_estudiante: int
    motivo_intervencion: str
    tipo_intervencion: str
    fecha_atencion: str
    seguimiento: Optional[str] = None

    @validator('id_estudiante')
    def validate_id_estudiante(cls, v):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser un número positivo')
        return v

    @validator('motivo_intervencion')
    def validate_motivo_intervencion(cls, v):
        if not validate_not_empty(v):
            raise ValueError('El motivo de intervención no puede estar vacío')
        if not validate_length(v, max_length=100):
            raise ValueError('El motivo de intervención no debe exceder los 100 caracteres')
        return v

    @validator('tipo_intervencion')
    def validate_tipo_intervencion(cls, v):
        if not validate_tipo_intervencion_pops(v):
            raise ValueError('Tipo de intervención inválido. Valores permitidos: Asesoría, Taller, Terapia individual, Asesoría grupal')
        return v

    @validator('fecha_atencion')
    def validate_fecha_atencion(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('seguimiento')
    def validate_seguimiento(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('El seguimiento no debe exceder los 255 caracteres')
        return v

class POPSCreate(POPSBase):
    """Esquema para crear un nuevo registro POPS."""
    pass

class POPSUpdate(BaseModel):
    """Esquema para actualizar un registro POPS existente."""
    motivo_intervencion: Optional[str] = None
    tipo_intervencion: Optional[str] = None
    fecha_atencion: Optional[str] = None
    seguimiento: Optional[str] = None

    @validator('motivo_intervencion')
    def validate_motivo_intervencion(cls, v):
        if v is not None:
            if not validate_not_empty(v):
                raise ValueError('El motivo de intervención no puede estar vacío')
            if not validate_length(v, max_length=100):
                raise ValueError('El motivo de intervención no debe exceder los 100 caracteres')
        return v

    @validator('tipo_intervencion')
    def validate_tipo_intervencion(cls, v):
        if v is not None and not validate_tipo_intervencion_pops(v):
            raise ValueError('Tipo de intervención inválido. Valores permitidos: Asesoría, Taller, Terapia individual, Asesoría grupal')
        return v

    @validator('fecha_atencion')
    def validate_fecha_atencion(cls, v):
        if v is not None and not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('seguimiento')
    def validate_seguimiento(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('El seguimiento no debe exceder los 255 caracteres')
        return v

print("Esquemas POPS cargados correctamente")