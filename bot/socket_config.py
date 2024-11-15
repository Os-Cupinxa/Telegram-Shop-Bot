import socketio

sio = socketio.AsyncClient()

BACKEND_URL = "http://localhost:8001"

async def connect_to_backend():
    print("Conectando ao backend via socket...")
    try:
        await sio.connect(BACKEND_URL)
        print("Conectado ao backend via socket.")
    except Exception as e:
        print(f"Erro ao conectar ao backend: {e}")

@sio.event
async def connect():
    print("Conexão estabelecida com o backend.")

@sio.event
async def disconnect():
    print("Desconectado do backend.")
