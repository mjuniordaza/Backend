from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EstudianteBase(BaseModel):
    id_estudiante: str
    nombres: str
    apellidos: str
    correo: str  # Cambiado de EmailStr a str simple
    semestre: str
    tipo_vulnerabilidad: Optional[str] = None
    riesgo_desercion: Optional[str] = None
    tipo_participante: Optional[str] = None
    riesgo_spadies: Optional[str] = None
    fecha_ingreso_programa: Optional[str] = None
    nivel_riesgo: Optional[str] = None
    requiere_tutoria: Optional[str] = None
    fecha_asignacion: Optional[str] = None
    tipo_intervencion: Optional[str] = None
    fecha_atencion: Optional[str] = None
    condicion_socioeconomica: Optional[str] = None
    fecha_solicitud: Optional[str] = None
    aprobado: Optional[str] = None

class EstudianteCreate(EstudianteBase):
    pass

class Estudiante(EstudianteBase):
    class Config:
        from_attributes = True  # Actualizado de orm_mode a from_attributes

class EstudianteList(BaseModel):
    estudiantes: List[Estudiante]

class CSVUploadResponse(BaseModel):
    filename: str
    estudiantes_cargados: int
    mensaje: str