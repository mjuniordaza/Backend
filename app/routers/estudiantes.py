from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List, Dict, Any

from app.services.estudiante_service import EstudianteService
from app.schemas.estudiante import Estudiante, EstudianteList, CSVUploadResponse

router = APIRouter()

# Dependencia para obtener el servicio de estudiantes
def get_estudiante_service():
    return EstudianteService()

@router.post("/estudiantes/upload-csv", response_model=CSVUploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    estudiante_service: EstudianteService = Depends(get_estudiante_service)
):
    """
    Carga un archivo CSV con datos de estudiantes.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
    result = await estudiante_service.process_csv_file(file)
    return result

@router.get("/estudiantes", response_model=List[Estudiante])
async def get_estudiantes(
    estudiante_service: EstudianteService = Depends(get_estudiante_service)
):
    """
    Obtiene todos los estudiantes cargados.
    """
    estudiantes = estudiante_service.get_all_estudiantes()
    return estudiantes

@router.get("/estudiantes/validados", response_model=List[Estudiante])
async def get_estudiantes_validados(
    estudiante_service: EstudianteService = Depends(get_estudiante_service)
):
    """
    Obtiene solo los estudiantes que pasan todas las validaciones.
    """
    estudiantes_validados = estudiante_service.get_estudiantes_validos()
    return estudiantes_validados

@router.get("/estudiantes/resumen-validacion")
async def get_resumen_validacion(
    estudiante_service: EstudianteService = Depends(get_estudiante_service)
):
    """
    Obtiene un resumen de la validación de estudiantes.
    """
    return estudiante_service.get_resumen_validacion()

@router.get("/estudiantes/{id_estudiante}", response_model=Estudiante)
async def get_estudiante(
    id_estudiante: str,
    estudiante_service: EstudianteService = Depends(get_estudiante_service)
):
    """
    Obtiene un estudiante por su ID.
    """
    estudiante = estudiante_service.get_estudiante_by_id(id_estudiante)
    return estudiante