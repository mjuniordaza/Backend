from pydantic import BaseModel, validator, Field
from typing import Optional
import sys
import os

# Añadir el directorio raíz al path para importar utils y base_schemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validators import *
from schemas.base_schemas import ServicioPermanenciaBase

class ComedorBase(BaseModel):
    """Esquema base para validación de datos del Comedor Universitario."""
    id_estudiante: int
    condicion_socioeconomica: str
    fecha_solicitud: str
    aprobado: bool
    observaciones: Optional[str] = None

    @validator('id_estudiante')
    def validate_id_estudiante(cls, v):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser un número positivo')
        return v

    @validator('condicion_socioeconomica')
    def validate_condicion_socioeconomica(cls, v):
        if not validate_not_empty(v):
            raise ValueError('La condición socioeconómica no puede estar vacía')
        if not validate_length(v, max_length=100):
            raise ValueError('La condición socioeconómica no debe exceder los 100 caracteres')
        return v

    @validator('fecha_solicitud')
    def validate_fecha_solicitud(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('observaciones')
    def validate_observaciones(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las observaciones no deben exceder los 255 caracteres')
        return v

class RegistroBeneficioBase(BaseModel):
    """Esquema base para validación de datos del Registro de Beneficio."""
    fecha_inscripcion: str
    estado_solicitud: bool
    periodo_academico: str
    fecha_inicio_servicio: str
    fecha_finalizacion_servicio: str
    numero_raciones_asignadas: int
    frecuencia_semanal: Optional[str] = None
    tipo_comida_recibida: str

    @validator('fecha_inscripcion', 'fecha_inicio_servicio', 'fecha_finalizacion_servicio')
    def validate_fechas(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('periodo_academico')
    def validate_periodo_academico(cls, v):
        if not validate_periodo_academico(v):
            raise ValueError('El periodo académico debe tener formato AAAA-N (ejemplo: 2023-1)')
        return v

    @validator('numero_raciones_asignadas')
    def validate_numero_raciones(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('El número de raciones debe ser un entero positivo')
        return v

    @validator('frecuencia_semanal')
    def validate_frecuencia_semanal(cls, v):
        if v is not None:
            allowed_frequencies = ['diaria', '3 veces por semana', '2 veces por semana', 'semanal']
            if not validate_enum(v, allowed_frequencies):
                raise ValueError(f'Frecuencia semanal inválida. Valores permitidos: {", ".join(allowed_frequencies)}')
        return v

    @validator('tipo_comida_recibida')
    def validate_tipo_comida(cls, v):
        allowed_types = ['Almuerzo', 'Cena', 'Desayuno']
        if not validate_enum(v, allowed_types):
            raise ValueError(f'Tipo de comida inválido. Valores permitidos: {", ".join(allowed_types)}')
        return v

    @validator('fecha_inicio_servicio')
    def validate_fecha_inicio(cls, v, values):
        if 'fecha_inscripcion' in values and v < values['fecha_inscripcion']:
            raise ValueError('La fecha de inicio del servicio no puede ser anterior a la fecha de inscripción')
        return v

    @validator('fecha_finalizacion_servicio')
    def validate_fecha_finalizacion(cls, v, values):
        if 'fecha_inicio_servicio' in values and v <= values['fecha_inicio_servicio']:
            raise ValueError('La fecha de finalización debe ser posterior a la fecha de inicio')
        return v

class ComedorCreate(ComedorBase):
    """Esquema para crear un nuevo registro de Comedor."""
    pass

class ComedorUpdate(BaseModel):
    """Esquema para actualizar un registro de Comedor existente."""
    condicion_socioeconomica: Optional[str] = None
    fecha_solicitud: Optional[str] = None
    aprobado: Optional[bool] = None
    observaciones: Optional[str] = None

    @validator('condicion_socioeconomica')
    def validate_condicion_socioeconomica(cls, v):
        if v is not None:
            if not validate_not_empty(v):
                raise ValueError('La condición socioeconómica no puede estar vacía')
            if not validate_length(v, max_length=100):
                raise ValueError('La condición socioeconómica no debe exceder los 100 caracteres')
        return v

    @validator('fecha_solicitud')
    def validate_fecha_solicitud(cls, v):
        if v is not None and not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('observaciones')
    def validate_observaciones(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las observaciones no deben exceder los 255 caracteres')
        return v

class RegistroBeneficioCreate(RegistroBeneficioBase):
    """Esquema para crear un nuevo registro de Beneficio."""
    pass

class RegistroBeneficioUpdate(BaseModel):
    """Esquema para actualizar un registro de Beneficio existente."""
    fecha_inscripcion: Optional[str] = None
    estado_solicitud: Optional[bool] = None
    periodo_academico: Optional[str] = None
    fecha_inicio_servicio: Optional[str] = None
    fecha_finalizacion_servicio: Optional[str] = None
    numero_raciones_asignadas: Optional[int] = None
    frecuencia_semanal: Optional
    numero_raciones_asignadas: Optional[int] = None
    frecuencia_semanal: Optional[str] = None
    tipo_comida_recibida: Optional[str] = None

    @validator('fecha_inscripcion', 'fecha_inicio_servicio', 'fecha_finalizacion_servicio')
    def validate_fechas(cls, v):
        if v is not None and not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('periodo_academico')
    def validate_periodo_academico(cls, v):
        if v is not None and not validate_periodo_academico(v):
            raise ValueError('El periodo académico debe tener formato AAAA-N (ejemplo: 2023-1)')
        return v

    @validator('numero_raciones_asignadas')
    def validate_numero_raciones(cls, v):
        if v is not None and (not isinstance(v, int) or v <= 0):
            raise ValueError('El número de raciones debe ser un entero positivo')
        return v

    @validator('frecuencia_semanal')
    def validate_frecuencia_semanal(cls, v):
        if v is not None:
            allowed_frequencies = ['diaria', '3 veces por semana', '2 veces por semana', 'semanal']
            if not validate_enum(v, allowed_frequencies):
                raise ValueError(f'Frecuencia semanal inválida. Valores permitidos: {", ".join(allowed_frequencies)}')
        return v

    @validator('tipo_comida_recibida')
    def validate_tipo_comida(cls, v):
        if v is not None:
            allowed_types = ['Almuerzo', 'Cena', 'Desayuno']
            if not validate_enum(v, allowed_types):
                raise ValueError(f'Tipo de comida inválido. Valores permitidos: {", ".join(allowed_types)}')
        return v

print("Esquemas Comedor cargados correctamente")