from services.validation_service import ValidationService

# Datos de ejemplo para un estudiante
estudiante_data = {
    "tipo_documento": "CC",
    "numero_documento": "1234567890",
    "nombres": "Juan Carlos",
    "apellidos": "Perez Gomez",
    "correo": "juan.perez@upc.edu.co",
    "telefono": "3001234567",
    "direccion": "Calle 15 #23-45, Valledupar",
    "programa_academico": "Ingenieria de Sistemas",
    "semestre": 5,
    "riesgo_desercion": "Bajo",
    "estrato": 3,
    "tipo_vulnerabilidad": "Economica"
}

# Datos de ejemplo para un registro POVAU
povau_data = {
    "id_estudiante": 1,
    "tipo_participante": "Nuevo",
    "riesgo_spadies": "Bajo",
    "fecha_ingreso_programa": "2023-02-15",
    "observaciones": "Estudiante con buen desempeño académico pero con dificultades economicas"
}

try:
    # Validar datos de estudiante
    validated_estudiante = ValidationService.validate_estudiante(estudiante_data)
    print("Datos de estudiante validados correctamente:")
    print(validated_estudiante)
    
    # Validar datos de POVAU
    validated_povau = ValidationService.validate_povau_create(povau_data)
    print("\nDatos de POVAU validados correctamente:")
    print(validated_povau)
    
    # Ejemplo con datos inválidos
    invalid_estudiante = {
        "tipo_documento": "XX",  # Tipo de documento inválido
        "numero_documento": "123",  # Número de documento muy corto
        "nombres": "123",  # Nombres con números
        "apellidos": "Perez Gomez",
        "correo": "correo_invalido",  # Correo inválido
        "telefono": "abc",  # Teléfono con letras
        "programa_academico": "Ingeniería de Sistemas",
        "semestre": 0,  # Semestre inválido
        "riesgo_desercion": "Desconocido",  # Riesgo inválido
        "estrato": 8,  # Estrato inválido
    }
    
    # Esto debería lanzar una excepción
    ValidationService.validate_estudiante(invalid_estudiante)
    
except ValueError as e:
    print("\nError de validacion:")
    print(e)


print("\nEjemplo de uso completado")