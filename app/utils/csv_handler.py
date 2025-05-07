import csv
import io
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

def parse_csv(file_content: bytes) -> List[Dict[str, Any]]:
    """
    Parsea el contenido de un archivo CSV y devuelve una lista de diccionarios.
    Cada diccionario representa una fila del CSV con las claves siendo los nombres de las columnas.
    """
    try:
        # Decodificar el contenido del archivo
        content = file_content.decode('utf-8')
        
        # Crear un objeto StringIO para leer el contenido como un archivo
        csv_file = io.StringIO(content)
        
        # Crear un lector CSV
        csv_reader = csv.DictReader(csv_file)
        
        # Convertir el lector CSV a una lista de diccionarios
        rows = list(csv_reader)
        
        logger.info(f"CSV parseado correctamente. {len(rows)} filas encontradas.")
        return rows
    
    except Exception as e:
        logger.error(f"Error al parsear el CSV: {str(e)}")
        raise ValueError(f"Error al parsear el CSV: {str(e)}")

def validate_csv_headers(headers: List[str], expected_headers: List[str]) -> bool:
    """
    Valida que los encabezados del CSV coincidan con los esperados.
    """
    # Verificar que todos los encabezados esperados estén presentes
    for header in expected_headers:
        if header not in headers:
            logger.warning(f"Encabezado esperado '{header}' no encontrado en el CSV.")
            return False
    
    logger.info("Encabezados del CSV validados correctamente.")
    return True