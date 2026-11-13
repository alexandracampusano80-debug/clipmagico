
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import uuid

app = FastAPI(title="ClipMágico API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def inicio():
    return {
        "app": "ClipMágico",
        "estado": "servidor funcionando"
    }

@app.get("/salud")
def salud():
    return {"ok": True}

@app.post("/subir-video")
async def subir_video(video: UploadFile = File(...)):
    extension = os.path.splitext(video.filename)[1].lower()

    if extension not in [".mp4", ".mov", ".mkv", ".webm"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato de video no permitido"}
        )

    nombre = f"{uuid.uuid4()}{extension}"
    ruta = os.path.join(UPLOAD_DIR, nombre)

    with open(ruta, "wb") as archivo:
        shutil.copyfileobj(video.file, archivo)

    return {
        "mensaje": "Video recibido correctamente",
        "archivo": nombre
    }
