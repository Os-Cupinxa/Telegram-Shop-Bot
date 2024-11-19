import httpx
import socketio

from env_config import SERVER_URL, TELEGRAM_API_URL

sio = socketio.AsyncClient()

BACKEND_URL = f"{SERVER_URL}/socket.io"

@sio.event
async def connect_to_backend():
    print("Connecting to backend socket...")
    print(f"Attempting to connect to: {BACKEND_URL}")
    try:
        await sio.connect(BACKEND_URL)
        print("Connection successful!")
    except Exception as e:
        print(f"Error while trying to connect to socket: {e}")



@sio.event
async def connect():
    print("Connected to backend socket.")


@sio.event
async def disconnect():
    print("Disconnected from backend socket.")

@sio.event
async def message(data):
    print(f"Message from server: {data}")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(f"{TELEGRAM_API_URL}/send_message", json=data)
    except Exception as e:
        print(f"Error while trying to send message to Telegram: {e}")