from typing import Dict, Any, List, Optional, Union, Type
from pydantic import BaseModel, ValidationError
import sys
import os

# Añadir el directorio raíz al path para importar schemas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.base_schemas import EstudianteBase, ServicioPermanenciaBase
from schemas.povau_schemas import POVAUCreate, POVAUUpdate
from schemas.poa_schemas import POACreate, POAUpdate
from schemas.pops_schemas import POPSCreate, POPSUpdate
from schemas.comedor_schemas import ComedorCreate, ComedorUpdate, RegistroBeneficioCreate, RegistroBeneficioUpdate

class ValidationService:
    """Servicio para validar datos antes de enviarlos a la base de datos."""
    
    @staticmethod
    def validate_data(data: Dict[str, Any], schema_class: Type[BaseModel]) -> Dict[str, Any]:
        """
        Valida los datos según el esquema proporcionado.
        
        Args:
            data: Diccionario con los datos a validar
            schema_class: Clase del esquema Pydantic a utilizar
            
        Returns:
            Diccionario con los datos validados
            
        Raises:
            ValueError: Si los datos no cumplen con las validaciones
        """
        try:
            # Crear instancia del esquema con los datos
            schema_instance = schema_class(**data)
            # Convertir a diccionario para devolver los datos validados
            return schema_instance.dict()
        except ValidationError as e:
            # Capturar errores de validación y lanzar una excepción con mensaje claro
            error_messages = []
            for error in e.errors():
                field = error["loc"][0]
                message = error["msg"]
                error_messages.append(f"Error en campo '{field}': {message}")
            
            raise ValueError("\n".join(error_messages))
    
    @staticmethod
    def validate_estudiante(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos de estudiante."""
        return ValidationService.validate_data(data, EstudianteBase)
    
    @staticmethod
    def validate_servicio_permanencia(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos de servicio de permanencia."""
        return ValidationService.validate_data(data, ServicioPermanenciaBase)
    
    @staticmethod
    def validate_povau_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para crear un registro POVAU."""
        return ValidationService.validate_data(data, POVAUCreate)
    
    @staticmethod
    def validate_povau_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para actualizar un registro POVAU."""
        return ValidationService.validate_data(data, POVAUUpdate)
    
    @staticmethod
    def validate_poa_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para crear un registro POA."""
        return ValidationService.validate_data(data, POACreate)
    
    @staticmethod
    def validate_poa_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para actualizar un registro POA."""
        return ValidationService.validate_data(data, POAUpdate)
    
    @staticmethod
    def validate_pops_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para crear un registro POPS."""
        return ValidationService.validate_data(data, POPSCreate)
    
    @staticmethod
    def validate_pops_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para actualizar un registro POPS."""
        return ValidationService.validate_data(data, POPSUpdate)
    
    @staticmethod
    def validate_comedor_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para crear un registro de Comedor."""
        return ValidationService.validate_data(data, ComedorCreate)
    
    @staticmethod
    def validate_comedor_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para actualizar un registro de Comedor."""
        return ValidationService.validate_data(data, ComedorUpdate)
    
    @staticmethod
    def validate_registro_beneficio_create(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para crear un registro de Beneficio."""
        return ValidationService.validate_data(data, RegistroBeneficioCreate)
    
    @staticmethod
    def validate_registro_beneficio_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """Valida datos para actualizar un registro de Beneficio."""
        return ValidationService.validate_data(data, RegistroBeneficioUpdate)
    
    @staticmethod
    def check_duplicates(data: Dict[str, Any], field: str, model, db_session) -> bool:
        """
        Verifica si ya existe un registro con el mismo valor en un campo específico.
        
        Args:
            data: Diccionario con los datos a verificar
            field: Nombre del campo a verificar duplicados
            model: Modelo de SQLAlchemy para la consulta
            db_session: Sesión de base de datos
            
        Returns:
            True si no hay duplicados, False si hay duplicados
        """
        if field not in data:
            return True
        
        value = data[field]
        query = db_session.query(model).filter(getattr(model, field) == value).first()
        return query is None

print("Servicio de validacion cargado correctamente")