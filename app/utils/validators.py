import re
from typing import Any, List, Optional, Dict, Union
from datetime import date

# Validadores generales
def validate_not_empty(value: Any) -> bool:
    """Valida que un valor no esté vacío."""
    if value is None:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True

def validate_length(value: str, min_length: int = 0, max_length: int = None) -> bool:
    """Valida que un string tenga la longitud adecuada."""
    if not isinstance(value, str):
        return False
    
    if len(value) < min_length:
        return False
    
    if max_length is not None and len(value) > max_length:
        return False
    
    return True

def validate_email(email: str) -> bool:
    """Valida que un email tenga formato correcto."""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_only_letters(text: str) -> bool:
    """Valida que un texto contenga solo letras y espacios."""
    if not text or not isinstance(text, str):
        return False
    
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
    return bool(re.match(pattern, text))

def validate_only_numbers(text: str) -> bool:
    """Valida que un texto contenga solo números."""
    if not text or not isinstance(text, str):
        return False
    
    return text.isdigit()

def validate_date_format(date_str: str) -> bool:
    """Valida que una fecha tenga formato YYYY-MM-DD."""
    if not date_str or not isinstance(date_str, str):
        return False
    
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        year, month, day = map(int, date_str.split('-'))
        date(year, month, day)
        return True
    except ValueError:
        return False

def validate_enum(value: str, allowed_values: List[str]) -> bool:
    """Valida que un valor esté dentro de una lista de valores permitidos."""
    return value in allowed_values

# Validadores específicos para los programas
def validate_tipo_documento(tipo: str) -> bool:
    """Valida que el tipo de documento sea valido."""
    allowed_types = ['CC', 'TI', 'CE', 'Pasaporte']
    return validate_enum(tipo, allowed_types)

def validate_estrato(estrato: int) -> bool:
    """Valida que el estrato esté entre 1 y 6."""
    return isinstance(estrato, int) and 1 <= estrato <= 6

def validate_semestre(semestre: int) -> bool:
    """Valida que el semestre sea un número positivo."""
    return isinstance(semestre, int) and semestre >= 1

def validate_riesgo_desercion(riesgo: str) -> bool:
    """Valida que el nivel de riesgo sea válido."""
    allowed_risks = ['Muy bajo', 'Bajo', 'Medio', 'Alto', 'Muy alto']
    return validate_enum(riesgo, allowed_risks)

def validate_estado_participacion(estado: str) -> bool:
    """Valida que el estado de participación sea válido."""
    allowed_states = ['Activo', 'Inactivo', 'Finalizado']
    return validate_enum(estado, allowed_states)

def validate_tipo_participante_povau(tipo: str) -> bool:
    """Valida que el tipo de participante POVAU sea válido."""
    allowed_types = ['Admitido', 'Nuevo', 'Media academica']
    return validate_enum(tipo, allowed_types)

def validate_tipo_intervencion_pops(tipo: str) -> bool:
    """Valida que el tipo de intervención POPS sea válido."""
    allowed_types = ['Asesoria', 'Taller', 'Terapia individual', 'Asesoria grupal']
    return validate_enum(tipo, allowed_types)

def validate_cumplimiento_requisitos(cumplimiento: str) -> bool:
    """Valida que el cumplimiento de requisitos sea válido."""
    allowed_values = ['Cumple', 'No cumple', 'Parcial']
    return validate_enum(cumplimiento, allowed_values)

def validate_periodo_academico(periodo: str) -> bool:
    """Valida que el periodo académico tenga formato AAAA-N."""
    if not periodo or not isinstance(periodo, str):
        return False
    
    pattern = r'^\d{4}-[1-2]$'
    return bool(re.match(pattern, periodo))

def validate_unique_in_database(value: Any, field: str, model, db_session) -> bool:
    """Valida que un valor sea único en la base de datos."""
    query = db_session.query(model).filter(getattr(model, field) == value).first()
    return query is None

print("Modulo de validacion cargado correctamente")