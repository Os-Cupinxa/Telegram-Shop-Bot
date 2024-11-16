import httpx
import socketio

sio = socketio.AsyncClient()

BACKEND_URL = "http://localhost:8001/socket.io"

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

@sio.event
async def new_message_to_bot(data):
    print("Message received:", data)

    chat_id = data['chat_id']
    message = data['message']

    payload = {
        'chat_id': chat_id,
        'text': message
    }

    async with httpx.AsyncClient() as client:
        from bot import TELEGRAM_API_URL
        await client.post(TELEGRAM_API_URL, params=payload)
