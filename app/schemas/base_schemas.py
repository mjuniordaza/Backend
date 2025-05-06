from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date
import sys
import os

# Añadir el directorio raíz al path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.validators import *

class EstudianteBase(BaseModel):
    """Esquema base para validación de datos de estudiante."""
    tipo_documento: str
    numero_documento: str
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    programa_academico: str
    semestre: int
    riesgo_desercion: str
    estrato: int
    tipo_vulnerabilidad: Optional[str] = None

    @validator('tipo_documento')
    def validate_tipo_documento(cls, v):
        if not validate_tipo_documento(v):
            raise ValueError(f'Tipo de documento inválido. Valores permitidos: CC, TI, CE, Pasaporte')
        return v

    @validator('numero_documento')
    def validate_numero_documento(cls, v):
        if not validate_not_empty(v):
            raise ValueError('El número de documento no puede estar vacío')
        if not validate_length(v, min_length=5, max_length=20):
            raise ValueError('El número de documento debe tener entre 5 y 20 caracteres')
        return v

    @validator('nombres', 'apellidos')
    def validate_nombres_apellidos(cls, v):
        if not validate_not_empty(v):
            raise ValueError('El nombre/apellido no puede estar vacío')
        if not validate_only_letters(v):
            raise ValueError('El nombre/apellido solo debe contener letras')
        if not validate_length(v, min_length=2, max_length=50):
            raise ValueError('El nombre/apellido debe tener entre 2 y 50 caracteres')
        return v

    @validator('telefono')
    def validate_telefono(cls, v):
        if v is not None:
            if not validate_only_numbers(v):
                raise ValueError('El teléfono solo debe contener números')
            if not validate_length(v, min_length=7, max_length=15):
                raise ValueError('El teléfono debe tener entre 7 y 15 caracteres')
        return v

    @validator('direccion')
    def validate_direccion(cls, v):
        if v is not None and not validate_length(v, max_length=100):
            raise ValueError('La dirección no debe exceder los 100 caracteres')
        return v

    @validator('programa_academico')
    def validate_programa_academico(cls, v):
        if not validate_not_empty(v):
            raise ValueError('El programa académico no puede estar vacío')
        return v

    @validator('semestre')
    def validate_semestre(cls, v):
        if not validate_semestre(v):
            raise ValueError('El semestre debe ser un número positivo')
        return v

    @validator('riesgo_desercion')
    def validate_riesgo_desercion(cls, v):
        if not validate_riesgo_desercion(v):
            raise ValueError('Nivel de riesgo inválido. Valores permitidos: Muy bajo, Bajo, Medio, Alto, Muy alto')
        return v

    @validator('estrato')
    def validate_estrato(cls, v):
        if not validate_estrato(v):
            raise ValueError('El estrato debe estar entre 1 y 6')
        return v

    @validator('tipo_vulnerabilidad')
    def validate_tipo_vulnerabilidad(cls, v):
        if v is not None:
            allowed_types = ['Economica', 'Academica', 'Psicosocial', 'Multiple']
            if not validate_enum(v, allowed_types):
                raise ValueError(f'Tipo de vulnerabilidad inválido. Valores permitidos: {", ".join(allowed_types)}')
        return v

class ServicioPermanenciaBase(BaseModel):
    """Esquema base para validación de servicios de permanencia."""
    id_estudiante: int
    servicio: str
    fecha_registro: str
    estado_participacion: str
    observaciones: Optional[str] = None

    @validator('id_estudiante')
    def validate_id_estudiante(cls, v):
        if v <= 0:
            raise ValueError('El ID del estudiante debe ser un número positivo')
        return v

    @validator('servicio')
    def validate_servicio(cls, v):
        allowed_services = ['POVAU', 'POA', 'POPS', 'Comedor']
        if not validate_enum(v, allowed_services):
            raise ValueError(f'Servicio inválido. Valores permitidos: {", ".join(allowed_services)}')
        return v

    @validator('fecha_registro')
    def validate_fecha_registro(cls, v):
        if not validate_date_format(v):
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v

    @validator('estado_participacion')
    def validate_estado_participacion(cls, v):
        if not validate_estado_participacion(v):
            raise ValueError('Estado de participación inválido. Valores permitidos: Activo, Inactivo, Finalizado')
        return v

    @validator('observaciones')
    def validate_observaciones(cls, v):
        if v is not None and not validate_length(v, max_length=255):
            raise ValueError('Las observaciones no deben exceder los 255 caracteres')
        return v

print("Esquemas base cargados correctamente")