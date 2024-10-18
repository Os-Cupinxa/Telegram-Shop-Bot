from sqlalchemy.orm import Session

from app.models import Order
from app.models.client_model import Client
from app.schemas.client_schema import ClientCreate
from app.services.global_service import get_object_by_id


def get_all_clients(db: Session):
    return db.query(Client).all()


def get_client(db: Session, client_id: int):
    db_client = get_object_by_id(db, Client, client_id, "Client not found")

    return db_client


def create_client(db: Session, client: ClientCreate):
    db_client = Client(
        name=client.name,
        phone_number=client.phone_number,
        city=client.city,
        address=client.address
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def update_client(db: Session, client_id: int, client: ClientCreate):
    db_client = get_object_by_id(db, Client, client_id, "Client not found")

    db_client.name = client.name
    db_client.phone_number=client.phone_number
    db_client.city=client.city
    db_client.address=client.address
    db_client.is_active=client.is_active
    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int):
    db_client = get_object_by_id(db, Client, client_id, "Client not found")

    orders = db.query(Order).filter(Order.client_id == client_id).first()

    if orders:
        return {"error": "Cannot delete client. There are orders associated with this client."}

    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted"}
