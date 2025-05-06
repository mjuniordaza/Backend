from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_service import leer_csv_temporal
import pandas as pd

router = APIRouter()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo debe ser .csv")

    # Leer el contenido del archivo subido
    try:
        contenido = await file.read()
        data = leer_csv_temporal(contenido)
        return {"datos": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando archivo: {e}")
