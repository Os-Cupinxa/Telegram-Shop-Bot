from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector

# Função para criar o banco de dados se ele não existir
def create_database_if_not_exists():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS telegramshopbot")
    conn.close()

# Chama a função para garantir que o banco de dados exista
create_database_if_not_exists()

# Configuração do SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/telegramshopbot"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria as tabelas automaticamente com base nos modelos
Base.metadata.create_all(bind=engine)
