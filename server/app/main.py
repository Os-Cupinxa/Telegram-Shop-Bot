from fastapi import FastAPI
from app.config.database import engine, Base
from app.controllers import user_controller, category_controller


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_controller.router)
app.include_router(category_controller.router)
