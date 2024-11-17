import httpx
import socketio

from env_config import SERVER_URL, TELEGRAM_API_URL

sio = socketio.AsyncClient()

BACKEND_URL = f"{SERVER_URL}/socket.io"


async def connect_to_backend():
    print("Connecting to backend socket...")
    try:
        await sio.connect(BACKEND_URL)
    except Exception as e:
        print(f"Error while trying to connect to socket: {e}")


@sio.event
async def connect():
    print("Connected to backend socket.")


@sio.event
async def disconnect():
    print("Disconnected from backend socket.")
