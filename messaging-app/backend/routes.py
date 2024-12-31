from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.auth_utils import hash_password, verify_password, create_access_token
from backend.crypto_utils import encrypt_message, decrypt_message, generate_aes_key
from backend.models import User, Message, SessionLocal
from Crypto.PublicKey import RSA

# Initialisation du routeur
router = APIRouter()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modèles Pydantic
class RegisterRequest(BaseModel):
    username: str
    password: str
    public_key: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SendMessageRequest(BaseModel):
    sender: str
    recipient: str
    message: str

# Route d'inscription
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        # Valider la clé publique RSA
        RSA.import_key(request.public_key)
    except ValueError:
        raise HTTPException(status_code=400, detail="Clé publique RSA non valide")

    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    
    hashed_password = hash_password(request.password)
    user = User(username=request.username, hashed_password=hashed_password, public_key=request.public_key)
    db.add(user)
    db.commit()
    return {"message": "Utilisateur enregistré avec succès"}

# Route de connexion
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Identifiants invalides")
    
    access_token = create_access_token(data={"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Route pour envoyer un message
@router.post("/send_message")
def send_message(request: SendMessageRequest, db: Session = Depends(get_db)):
    recipient_user = db.query(User).filter(User.username == request.recipient).first()
    if not recipient_user:
        raise HTTPException(status_code=404, detail="Destinataire introuvable")

    try:
        aes_key = generate_aes_key()
        encrypted_aes_key = encrypt_message(aes_key, recipient_user.public_key)
        encrypted_message = encrypt_message(request.message, aes_key)

        new_message = Message(
            sender=request.sender,
            recipient=request.recipient,
            encrypted_key=encrypted_aes_key,
            encrypted_message=encrypted_message
        )
        db.add(new_message)
        db.commit()
        return {"message": "Message envoyé avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chiffrement : {str(e)}")

# Route pour récupérer les messages
@router.get("/get_messages/{username}")
def get_messages(username: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.recipient == username).all()
    if not messages:
        raise HTTPException(status_code=404, detail="Aucun message trouvé")
    return messages
