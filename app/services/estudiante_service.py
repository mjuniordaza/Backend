from typing import List, Dict, Any, Optional, Set
import logging
import re
from datetime import datetime
from fastapi import UploadFile, HTTPException

from app.models.estudiante import EstudianteModel, EstudianteStore
from app.utils.csv_handler import parse_csv, validate_csv_headers
from app.schemas.estudiante import Estudiante

logger = logging.getLogger(__name__)

# Lista de encabezados esperados en el CSV
EXPECTED_HEADERS = [
    "id_estudiante", "nombres", "apellidos", "correo", "semestre", 
    "tipo_vulnerabilidad", "riesgo_desercion", "tipo_participante", 
    "riesgo_spadies", "fecha_ingreso_programa", "nivel_riesgo", 
    "requiere_tutoria", "fecha_asignacion", "tipo_intervencion", 
    "fecha_atencion", "condicion_socioeconomica", "fecha_solicitud", "aprobado"
]

# Valores permitidos según el diccionario de datos
VALORES_PERMITIDOS = {
    "tipo_vulnerabilidad": ["Económica", "Académica", "Psicosocial", "Múltiple", None, ""],
    "riesgo_desercion": ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto", None, ""],
    "tipo_participante": ["Admitido", "Nuevo", "Media académica", None, ""],
    "riesgo_spadies": ["Bajo", "Medio", "Alto", None, ""],
    "nivel_riesgo": ["Muy bajo", "Bajo", "Medio", "Alto", "Muy alto", None, ""],
    "requiere_tutoria": ["true", "false", "True", "False", None, ""],
    "tipo_intervencion": ["Asesoría", "Taller", "Otro", None, ""],
    "condicion_socioeconomica": ["Económica", "Múltiple", None, ""],
    "aprobado": ["true", "false", "True", "False", None, ""]
}

class EstudianteService:
    def __init__(self):
        self.store = EstudianteStore()
    
    async def process_csv_file(self, file: UploadFile) -> Dict[str, Any]:
        """
        Procesa un archivo CSV y carga los datos en el almacén sin validación.
        """
        try:
            # Leer el contenido del archivo
            file_content = await file.read()
            
            # Parsear el CSV
            rows = parse_csv(file_content)
            
            if not rows:
                raise HTTPException(status_code=400, detail="El archivo CSV está vacío")
            
            # Validar solo que los encabezados existan
            if not validate_csv_headers(rows[0].keys(), EXPECTED_HEADERS):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Los encabezados del CSV no coinciden con los esperados. Esperados: {', '.join(EXPECTED_HEADERS)}"
                )
            
            # Limpiar el almacén antes de cargar nuevos datos
            self.store.clear_estudiantes()
            
            # Procesar cada fila y crear objetos EstudianteModel sin validación
            for row in rows:
                estudiante = EstudianteModel(
                    id_estudiante=row.get("id_estudiante", ""),
                    nombres=row.get("nombres", ""),
                    apellidos=row.get("apellidos", ""),
                    correo=row.get("correo", ""),  # Sin validación
                    semestre=row.get("semestre", ""),
                    tipo_vulnerabilidad=row.get("tipo_vulnerabilidad"),
                    riesgo_desercion=row.get("riesgo_desercion"),
                    tipo_participante=row.get("tipo_participante"),
                    riesgo_spadies=row.get("riesgo_spadies"),
                    fecha_ingreso_programa=row.get("fecha_ingreso_programa"),
                    nivel_riesgo=row.get("nivel_riesgo"),
                    requiere_tutoria=row.get("requiere_tutoria"),
                    fecha_asignacion=row.get("fecha_asignacion"),
                    tipo_intervencion=row.get("tipo_intervencion"),
                    fecha_atencion=row.get("fecha_atencion"),
                    condicion_socioeconomica=row.get("condicion_socioeconomica"),
                    fecha_solicitud=row.get("fecha_solicitud"),
                    aprobado=row.get("aprobado")
                )
                self.store.add_estudiante(estudiante)
            
            logger.info(f"CSV procesado correctamente. {len(rows)} estudiantes cargados sin validación.")
            
            return {
                "filename": file.filename,
                "estudiantes_cargados": len(rows),
                "mensaje": "Archivo CSV procesado correctamente. Datos cargados sin validación."
            }
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error al procesar el archivo CSV: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error al procesar el archivo CSV: {str(e)}")
    
    def get_all_estudiantes(self) -> List[EstudianteModel]:
        """
        Obtiene todos los estudiantes del almacén.
        """
        return self.store.get_all_estudiantes()
    
    def get_estudiante_by_id(self, id_estudiante: str) -> Optional[EstudianteModel]:
        """
        Obtiene un estudiante por su ID.
        """
        estudiante = self.store.get_estudiante_by_id(id_estudiante)
        if not estudiante:
            raise HTTPException(status_code=404, detail=f"Estudiante con ID {id_estudiante} no encontrado")
        return estudiante
    
    def validate_estudiantes(self) -> Dict[str, Any]:
        """
        Valida los estudiantes cargados según el diccionario de datos,
        elimina duplicados y devuelve solo los registros válidos.
        """
        estudiantes_validos = []
        estudiantes_invalidos = []
        errores_por_campo = {}
        ids_procesados = set()  # Para detectar duplicados por ID
        correos_procesados = set()  # Para detectar duplicados por correo
        
        # Obtener todos los estudiantes cargados
        todos_estudiantes = self.store.get_all_estudiantes()
        
        for estudiante in todos_estudiantes:
            # Inicializar variables para el seguimiento de errores
            es_valido = True
            errores = []
            
            # 1. Validar campos requeridos
            if not estudiante.id_estudiante:
                es_valido = False
                errores.append("ID de estudiante es requerido")
                self._agregar_error_campo(errores_por_campo, "id_estudiante", "Campo requerido")
            
            if not estudiante.nombres:
                es_valido = False
                errores.append("Nombres es requerido")
                self._agregar_error_campo(errores_por_campo, "nombres", "Campo requerido")
            elif not self._validar_solo_letras(estudiante.nombres):
                es_valido = False
                errores.append("Nombres debe contener solo letras")
                self._agregar_error_campo(errores_por_campo, "nombres", "Solo letras permitidas")
            
            if not estudiante.apellidos:
                es_valido = False
                errores.append("Apellidos es requerido")
                self._agregar_error_campo(errores_por_campo, "apellidos", "Campo requerido")
            elif not self._validar_solo_letras(estudiante.apellidos):
                es_valido = False
                errores.append("Apellidos debe contener solo letras")
                self._agregar_error_campo(errores_por_campo, "apellidos", "Solo letras permitidas")
            
            if not estudiante.correo:
                es_valido = False
                errores.append("Correo es requerido")
                self._agregar_error_campo(errores_por_campo, "correo", "Campo requerido")
            elif not self._validar_correo(estudiante.correo):
                es_valido = False
                errores.append("Formato de correo inválido")
                self._agregar_error_campo(errores_por_campo, "correo", "Formato inválido")
            
            if not estudiante.semestre:
                es_valido = False
                errores.append("Semestre es requerido")
                self._agregar_error_campo(errores_por_campo, "semestre", "Campo requerido")
            
            # 2. Validar valores permitidos según el diccionario de datos
            for campo, valores_permitidos in VALORES_PERMITIDOS.items():
                valor = getattr(estudiante, campo, None)
                if valor is not None and valor not in valores_permitidos:
                    es_valido = False
                    errores.append(f"{campo} tiene un valor no permitido: {valor}")
                    self._agregar_error_campo(errores_por_campo, campo, f"Valor no permitido: {valor}")
            
            # 3. Validar fechas
            campos_fecha = ["fecha_ingreso_programa", "fecha_asignacion", "fecha_atencion", "fecha_solicitud"]
            for campo in campos_fecha:
                valor = getattr(estudiante, campo, None)
                if valor and not self._validar_fecha(valor):
                    es_valido = False
                    errores.append(f"{campo} tiene un formato de fecha inválido: {valor}")
                    self._agregar_error_campo(errores_por_campo, campo, "Formato de fecha inválido")
            
            # 4. Verificar duplicados
            if estudiante.id_estudiante in ids_procesados:
                es_valido = False
                errores.append(f"ID de estudiante duplicado: {estudiante.id_estudiante}")
                self._agregar_error_campo(errores_por_campo, "id_estudiante", "Valor duplicado")
            
            if estudiante.correo and estudiante.correo in correos_procesados:
                es_valido = False
                errores.append(f"Correo electrónico duplicado: {estudiante.correo}")
                self._agregar_error_campo(errores_por_campo, "correo", "Valor duplicado")
            
            # Si el registro es válido, añadirlo a la lista de válidos y registrar IDs procesados
            if es_valido:
                estudiantes_validos.append(estudiante)
                if estudiante.id_estudiante:
                    ids_procesados.add(estudiante.id_estudiante)
                if estudiante.correo:
                    correos_procesados.add(estudiante.correo)
            else:
                # Guardar el estudiante inválido junto con sus errores
                estudiantes_invalidos.append({
                    "estudiante": estudiante,
                    "errores": errores
                })
        
        # Registrar resultados en el log
        total = len(todos_estudiantes)
        validos = len(estudiantes_validos)
        invalidos = len(estudiantes_invalidos)
        
        logger.info(f"Validación completada: {validos} válidos, {invalidos} inválidos de un total de {total}")
        
        # Devolver resultados detallados
        return {
            "estudiantes_validos": estudiantes_validos,
            "total_registros": total,
            "registros_validos": validos,
            "registros_invalidos": invalidos,
            "errores_por_campo": errores_por_campo,
            "detalle_invalidos": estudiantes_invalidos
        }
    
    def _agregar_error_campo(self, errores_por_campo: Dict[str, Dict[str, int]], campo: str, error: str) -> None:
        """
        Agrega un error al diccionario de errores por campo.
        """
        if campo not in errores_por_campo:
            errores_por_campo[campo] = {}
        
        if error not in errores_por_campo[campo]:
            errores_por_campo[campo][error] = 0
        
        errores_por_campo[campo][error] += 1
    
    def _validar_solo_letras(self, texto: str) -> bool:
        """
        Valida que un texto contenga solo letras, espacios y caracteres acentuados.
        """
        if not texto:
            return False
        
        # Expresión regular que permite letras (incluyendo acentuadas), espacios y algunos caracteres especiales
        patron = r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s\'\-\.]+$'
        return bool(re.match(patron, texto))
    
    def _validar_correo(self, correo: str) -> bool:
        """
        Valida que un texto tenga formato de correo electrónico.
        """
        if not correo:
            return False
        
        # Expresión regular para validar correos electrónicos
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, correo))
    
    def _validar_fecha(self, fecha_str: str) -> bool:
        """
        Valida que un texto tenga formato de fecha válido.
        """
        if not fecha_str:
            return False
        
        # Intentar varios formatos de fecha comunes
        formatos = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y', '%Y/%m/%d']
        
        for formato in formatos:
            try:
                datetime.strptime(fecha_str, formato)
                return True
            except ValueError:
                continue
        
        return False
    
    def get_estudiantes_validos(self) -> List[EstudianteModel]:
        """
        Obtiene solo los estudiantes que pasan todas las validaciones.
        """
        resultado = self.validate_estudiantes()
        return resultado["estudiantes_validos"]
    
    def get_resumen_validacion(self) -> Dict[str, Any]:
        """
        Obtiene un resumen de la validación sin incluir los datos completos.
        """
        resultado = self.validate_estudiantes()
        
        # Excluir los datos completos para hacer el resumen más ligero
        del resultado["estudiantes_validos"]
        del resultado["detalle_invalidos"]
        
        return resultado