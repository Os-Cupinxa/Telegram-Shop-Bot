import re

import httpx
from telegram import Update
from telegram.ext import ContextTypes


async def finish_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Por favor, digite seu CPF para finalizar o pedido:")

    context.user_data['awaiting_cpf'] = True


async def process_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw_cpf = update.message.text
    cpf = re.sub(r'[.-]', '', raw_cpf)

    context.user_data['cpf'] = cpf

    await check_user_by_cpf(update, context)

    context.user_data['awaiting_cpf'] = False


async def check_user_by_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cpf = context.user_data.get('cpf')
    url = f"http://127.0.0.1:8001/clients/cpf/{cpf}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        client_data = response.json()
        await update.message.reply_text(f"Cliente encontrado:\n{client_data}")
    else:
        await update.message.reply_text("Cliente não encontrado. Encerrando a conversa.")
