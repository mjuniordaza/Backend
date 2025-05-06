from pydantic import BaseModel, validator, Field
from typing import Optional, List
import sys
import os

# Añadir el directorio raíz al path para importar utils y base_schemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validators import *
from schemas.base_schemas import ServicioPermanenciaBase

class POABase(BaseModel):
    """Esquema base para validación de datos POA."""
    id_estudiante: int
    nivel_riesgo: str
    requiere_tutoria: bool
    fecha_asignacion: str
    acciones_apoyo: Optional[str] = None

    @validator('id_estudiante')
    def validate_id_estudiante(cls, v):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser un número positivo')
        return v

    @validator('nivel_riesgo')
    def validate_nivel_riesgo(cls, v):
        if not validate_riesgo_desercion(v):
            raise ValueError('Nivel de riesgo inválido. Valores permitidos: Muy bajo, Bajo, Medio, Alto, Muy alto')
        return v

    @validator('fecha_asignacion')
    def validate_fecha_asignacion(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('acciones_apoyo')
    def validate_acciones_apoyo(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las acciones de apoyo no deben exceder los 255 caracteres')
        return v

class POACreate(POABase):
    """Esquema para crear un nuevo registro POA."""
    pass

class POAUpdate(BaseModel):
    """Esquema para actualizar un registro POA existente."""
    nivel_riesgo: Optional[str] = None
    requiere_tutoria: Optional[bool] = None
    fecha_asignacion: Optional[str] = None
    acciones_apoyo: Optional[str] = None

    @validator('nivel_riesgo')
    def validate_nivel_riesgo(cls, v):
        if v is not None and not validate_riesgo_desercion(v):
            raise ValueError('Nivel de riesgo inválido. Valores permitidos: Muy bajo, Bajo, Medio, Alto, Muy alto')
        return v

    @validator('fecha_asignacion')
    def validate_fecha_asignacion(cls, v):
        if v is not None and not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('acciones_apoyo')
    def validate_acciones_apoyo(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las acciones de apoyo no deben exceder los 255 caracteres')
        return v

print("Esquemas POA cargados correctamente")