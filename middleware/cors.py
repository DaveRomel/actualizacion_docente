from fastapi.middleware.cors import CORSMiddleware

#Ejemplo de como debe pasarse origenes permitidos
origins = [
    "http://localhost",
    "http://127.0.0.1:4000",
    "http://localhost:4000",
    "http://localhost:5173",
]

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,  # Si usas JWT o sesiones
        allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
        allow_headers=["*"],  # Permite cualquier header
    )
