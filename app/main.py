from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import estudiantes

app = FastAPI(
    title="API de Estudiantes",
    description="API para cargar y gestionar datos de estudiantes desde CSV",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(estudiantes.router, prefix="/api", tags=["estudiantes"])

@app.get("/")
async def root():
    return {"message": "API de Estudiantes funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)