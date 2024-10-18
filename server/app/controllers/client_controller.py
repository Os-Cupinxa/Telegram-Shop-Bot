from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.client_schema import ClientCreate, ClientResponse
from app.services import client_service
from app.config.database import get_db

router = APIRouter()


@router.get("/clients/", response_model=List[ClientResponse], tags=["Clients"])
def read_clients(db: Session = Depends(get_db)):
    return client_service.get_all_clients(db)


@router.get("/clients/{client_id}", response_model=ClientResponse, tags=["Clients"])
def read_client(client_id: int, db: Session = Depends(get_db)):
    return client_service.get_client(db, client_id)


@router.post("/clients/", response_model=ClientResponse, tags=["Clients"])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    return client_service.create_client(db, client)


@router.put("/clients/", response_model=ClientResponse, tags=["Clients"])
def update_client(client_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    return client_service.update_client(db, client_id, client)


@router.delete("/clients/{client_id}", tags=["Clients"])
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return client_service.delete_client(db, client_id)
