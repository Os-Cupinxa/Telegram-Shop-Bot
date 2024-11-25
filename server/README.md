# Como rodar o servidor

## Instalar dependências:

```bash
pip install -r requirements.txt
```

## Verifique se já existe um processo rodando na porta 8000:

```bash
netstat -ano | findstr :8001
```

## Encerre o Processo (se necessário)::

```bash
taskkill /PID <PID> /F
```

## Rodar o servidor FastAPI:

```bash
python -m uvicorn app.main:app --reload --port 8001
```

## Swagger do FastAPI:

[Swagger FastAPI](http://127.0.0.1:8001/docs)

## Para rodar o seeder:

```bash
python app/seeders/seeder.py
```
