# main.py
"""Responsabilidad: Punto de entrada de la aplicación FastAPI.

Define la instancia de FastAPI.

Incluye los routers (include_router).

Configura middlewares y otras inicializaciones.
"""
from fastapi import FastAPI
from app.routers import upload

app = FastAPI()

app.include_router(upload.router, prefix="/api", tags=["Subida de CSV"])


