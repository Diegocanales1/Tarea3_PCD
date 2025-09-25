from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Se conecta a una base de datos SQLite en un archivo llamado users.db
DATABASE_URL = "sqlite:///./users.db"

# Crea el motor de la base de datos
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def create_tables():
    """
    Crea las tablas en la base de datos si no existen.
    """
    Base.metadata.create_all(bind=engine)

