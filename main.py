from fastapi import FastAPI
from router.router import user
from auth import auth
from middleware.cors import setup_cors
from router.materias import materia
from router.inscripcion import inscripcion

app=FastAPI()

setup_cors(app)

app.include_router(user, tags=["user"])
app.include_router(materia, tags=["materia"])
app.include_router(auth, tags=["auth"])
app.include_router(inscripcion, tags=["inscripcion"])

@app.get("/")
def root():
    return "El proyecto esta en linea."
