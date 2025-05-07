from datetime import datetime
from typing import Optional, List

# Clase para almacenar los datos de estudiantes en memoria
class EstudianteModel:
    def __init__(self, 
                 id_estudiante: str,
                 nombres: str,
                 apellidos: str,
                 correo: str,
                 semestre: str,
                 tipo_vulnerabilidad: Optional[str] = None,
                 riesgo_desercion: Optional[str] = None,
                 tipo_participante: Optional[str] = None,
                 riesgo_spadies: Optional[str] = None,
                 fecha_ingreso_programa: Optional[str] = None,
                 nivel_riesgo: Optional[str] = None,
                 requiere_tutoria: Optional[str] = None,
                 fecha_asignacion: Optional[str] = None,
                 tipo_intervencion: Optional[str] = None,
                 fecha_atencion: Optional[str] = None,
                 condicion_socioeconomica: Optional[str] = None,
                 fecha_solicitud: Optional[str] = None,
                 aprobado: Optional[str] = None):
        self.id_estudiante = id_estudiante
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.semestre = semestre
        self.tipo_vulnerabilidad = tipo_vulnerabilidad
        self.riesgo_desercion = riesgo_desercion
        self.tipo_participante = tipo_participante
        self.riesgo_spadies = riesgo_spadies
        self.fecha_ingreso_programa = fecha_ingreso_programa
        self.nivel_riesgo = nivel_riesgo
        self.requiere_tutoria = requiere_tutoria
        self.fecha_asignacion = fecha_asignacion
        self.tipo_intervencion = tipo_intervencion
        self.fecha_atencion = fecha_atencion
        self.condicion_socioeconomica = condicion_socioeconomica
        self.fecha_solicitud = fecha_solicitud
        self.aprobado = aprobado

# Almacén de datos en memoria
class EstudianteStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EstudianteStore, cls).__new__(cls)
            cls._instance.estudiantes = []
        return cls._instance
    
    def add_estudiante(self, estudiante: EstudianteModel):
        self.estudiantes.append(estudiante)
    
    def get_all_estudiantes(self) -> List[EstudianteModel]:
        return self.estudiantes
    
    def clear_estudiantes(self):
        self.estudiantes = []
    
    def get_estudiante_by_id(self, id_estudiante: str) -> Optional[EstudianteModel]:
        for estudiante in self.estudiantes:
            if estudiante.id_estudiante == id_estudiante:
                return estudiante
        return None