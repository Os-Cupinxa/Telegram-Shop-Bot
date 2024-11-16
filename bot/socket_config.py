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


import re


def escape_markdown(text: str) -> str:
    escape_chars = r"([_*\[\]()~`>#+\-=|{}.!])"
    return re.sub(escape_chars, r"\\\1", text)


@sio.event
async def new_message_to_bot(data):
    print("Message received:", data)

    chat_id = data['chat_id']
    message = data['message']
    user_name = data['user_name']

    # Escapar caracteres problemáticos
    escaped_user_name = escape_markdown(user_name)
    escaped_message = escape_markdown(message)

    # Formatar a mensagem com o nome em negrito
    formatted_message = f"*{escaped_user_name}:*\n{escaped_message}"

    payload = {
        'chat_id': chat_id,
        'text': formatted_message,
        'parse_mode': 'Markdown'  # Especifica que o texto usa Markdown
    }

    async with httpx.AsyncClient() as client:
        from bot import TELEGRAM_API_URL
        response = await client.post(TELEGRAM_API_URL, params=payload)
        if response.status_code == 200:
            print(f"Message successfully sent to chat_id {chat_id}")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
