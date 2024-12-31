from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Base, engine
from backend.routes import router

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Changez pour spécifier les origines autorisées si nécessaire
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Création des tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

# Enregistrement des routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "API de messagerie sécurisée opérationnelle"}
