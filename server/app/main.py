import socketio
from fastapi import FastAPI
from app.config.database import engine, Base
from app.controllers import (user_controller,
                             category_controller,
                             product_controller,
                             order_controller,
                             client_controller,
                             message_controller, auth_controller)

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Auth"},
    {"name": "Users"},
    {"name": "Categories"},
    {"name": "Products"},
    {"name": "Orders"},
    {"name": "Clients"},
    {"name": "Messages"},
]

app = FastAPI(
    title="Telegram Shop Bot API",
    version="1.0.0",
    openapi_tags=tags_metadata
)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
socket_app = socketio.ASGIApp(sio)

app.include_router(auth_controller.router)
app.include_router(user_controller.router)
app.include_router(category_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)
app.include_router(client_controller.router)
app.include_router(message_controller.router)


@app.on_event("startup")
async def startup_event():
    print("\033[92mINFO:\033[0m     Socket server has started.")


@app.on_event("shutdown")
async def shutdown_event():
    print("\033[92mINFO:\033[0m     Socket server is shutting down.")


@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")


@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit("response", {"message": "Message received!"})


app.mount("/socket.io", socket_app)
