from fastapi import FastAPI
from app.config.database import engine, Base
from app.controllers import user_controller, category_controller, product_controller, order_controller, client_controller

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Users"
    },
    {
        "name": "Categories"
    },
    {
        "name": "Products"
    },
    {
        "name": "Orders"
    },
    {
        "name": "Clients"
    }
]

app = FastAPI(
    title="Telegram Shop Bot API",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(user_controller.router)
app.include_router(category_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)
app.include_router(client_controller.router)
