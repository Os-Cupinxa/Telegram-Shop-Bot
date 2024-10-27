import httpx
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from bot import CHECK_USER_BY_CPF, ALREADY_REGISTERED


async def already_registered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('already_registered chamado')
    cpf_input = update.message.text

    print(cpf_input)
    print(cpf_input.isdigit())
    print(len(cpf_input))

    if cpf_input.isdigit() and len(cpf_input) == 11:
        context.user_data['cpf'] = cpf_input
        await check_user_by_cpf(update, context)
        return CHECK_USER_BY_CPF
    else:
        await update.message.reply_text("Por favor, informe um CPF válido com 11 dígitos.")
        return ALREADY_REGISTERED


async def check_user_by_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('check_user_by_cpf chamado')

    cpf = context.user_data.get('cpf')
    print("check_user_by_cpf chamado")
    print(f"CPF recebido: {cpf}")
    url = f"http://127.0.0.1:8001/clients/cpf/{cpf}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        client_data = response.json()
        await update.message.reply_text(f"Cliente encontrado:\n{client_data}")
    else:
        await update.message.reply_text("Cliente não encontrado. Encerrando a conversa.")

    return ConversationHandler.END
