# csv_service.py
"""
Responsabilidad: Lógica de negocio directamente relacionada con manipulación del archivo CSV.

Leer, escribir, actualizar y borrar registros.

Funciones como cargar_datos(), guardar_datos(), agregar_usuario(), etc.
"""
import pandas as pd
from io import StringIO

def leer_csv_temporal(contenido: bytes):
    """
    Lee un archivo CSV en memoria desde bytes y lo retorna como lista de dicts.
    """
    try:
        archivo_str = contenido.decode("utf-8")
        df = pd.read_csv(StringIO(archivo_str))
        return df.to_dict(orient="records")
    except Exception as e:
        raise ValueError(f"Error leyendo CSV: {e}")
