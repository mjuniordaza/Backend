from pydantic import BaseModel, validator, Field
from typing import Optional
import sys
import os

# Añadir el directorio raíz al path para importar utils y base_schemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validators import *
from schemas.base_schemas import ServicioPermanenciaBase

class POVAUBase(BaseModel):
    """Esquema base para validación de datos POVAU."""
    id_estudiante: int
    tipo_participante: str
    riesgo_spadies: str
    fecha_ingreso_programa: str
    observaciones: Optional[str] = None

    @validator('id_estudiante')
    def validate_id_estudiante(cls, v):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser un número positivo')
        return v

    @validator('tipo_participante')
    def validate_tipo_participante(cls, v):
        if not validate_tipo_participante_povau(v):
            raise ValueError('Tipo de participante inválido. Valores permitidos: Admitido, Nuevo, Media académica')
        return v

    @validator('riesgo_spadies')
    def validate_riesgo_spadies(cls, v):
        allowed_risks = ['Bajo', 'Medio', 'Alto']
        if not validate_enum(v, allowed_risks):
            raise ValueError(f'Riesgo SPADIES inválido. Valores permitidos: {", ".join(allowed_risks)}')
        return v

    @validator('fecha_ingreso_programa')
    def validate_fecha_ingreso_programa(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('observaciones')
    def validate_observaciones(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las observaciones no deben exceder los 255 caracteres')
        return v

class POVAUCreate(POVAUBase):
    """Esquema para crear un nuevo registro POVAU."""
    pass

class POVAUUpdate(BaseModel):
    """Esquema para actualizar un registro POVAU existente."""
    tipo_participante: Optional[str] = None
    riesgo_spadies: Optional[str] = None
    fecha_ingreso_programa: Optional[str] = None
    observaciones: Optional[str] = None

    @validator('tipo_participante')
    def validate_tipo_participante(cls, v):
        if v is not None and not validate_tipo_participante_povau(v):
            raise ValueError('Tipo de participante inválido. Valores permitidos: Admitido, Nuevo, Media académica')
        return v

    @validator('riesgo_spadies')
    def validate_riesgo_spadies(cls, v):
        if v is not None:
            allowed_risks = ['Bajo', 'Medio', 'Alto']
            if not validate_enum(v, allowed_risks):
                raise ValueError(f'Riesgo SPADIES inválido. Valores permitidos: {", ".join(allowed_risks)}')
        return v

    @validator('fecha_ingreso_programa')
    def validate_fecha_ingreso_programa(cls, v):
        if v is not None and not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('observaciones')
    def validate_observaciones(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las observaciones no deben exceder los 255 caracteres')
        return v

print("Esquemas POVAU cargados correctamente")