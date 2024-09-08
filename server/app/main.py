from fastapi import FastAPI
from app.config.database import engine, Base
from app.controllers import user_controller, category_controller

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Users"
    },
    {
        "name": "Categories"
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
