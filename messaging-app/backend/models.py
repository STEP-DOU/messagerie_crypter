from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuration de la base SQLite
DATABASE_URL = "sqlite:///./messaging_app.db"

# Création du moteur de base de données
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle pour les utilisateurs
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    public_key = Column(Text)

# Modèle pour les messages
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    recipient = Column(String)
    encrypted_key = Column(Text)  # Clé AES chiffrée avec RSA
    encrypted_message = Column(Text)  # Message chiffré avec AES
