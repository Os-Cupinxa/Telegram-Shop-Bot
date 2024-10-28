import httpx
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot import CHECK_USER_BY_CPF, ALREADY_REGISTERED, REGISTERING_PROCESS


async def already_registered(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cpf_input = update.message.text

    if cpf_input.isdigit() and len(cpf_input) == 11:
        context.user_data['cpf'] = cpf_input
        await check_user_by_cpf(update, context)
        return CHECK_USER_BY_CPF
    else:
        await update.message.reply_text("Por favor, informe um CPF válido com 11 dígitos.")
        return ALREADY_REGISTERED


async def check_user_by_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    cpf = context.user_data.get('cpf')
    url = f"http://127.0.0.1:8001/clients/cpf/{cpf}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        client_data = response.json()
        await update.message.reply_text(f"Cliente encontrado:\n{client_data}")
    else:
        await update.message.reply_text("Cliente não encontrado. Encerrando a conversa.")

    return ConversationHandler.END


async def registering_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Inicializando o passo se não existir
    if "registering_step" not in context.user_data:
        context.user_data["registering_step"] = 0

    step = context.user_data["registering_step"]

    if step == 0:
        await update.message.reply_text("Vamos iniciar o seu cadastro! Por favor, informe seu nome.")
        context.user_data["registering_step"] += 1
        return REGISTERING_PROCESS

    elif step == 1:
        context.user_data["name"] = update.message.text
        await update.message.reply_text("Ótimo! Agora, informe seu CPF.")
        context.user_data["registering_step"] += 1
        return REGISTERING_PROCESS

    elif step == 2:
        context.user_data["cpf"] = update.message.text
        await update.message.reply_text("Perfeito! Agora, informe seu número de telefone.")
        context.user_data["registering_step"] += 1
        return REGISTERING_PROCESS

    elif step == 3:
        context.user_data["phone_number"] = update.message.text
        await update.message.reply_text("Quase lá! Agora, informe sua cidade.")
        context.user_data["registering_step"] += 1
        return REGISTERING_PROCESS

    elif step == 4:
        context.user_data["city"] = update.message.text
        await update.message.reply_text("Por último, informe seu endereço.")
        context.user_data["registering_step"] += 1
        return REGISTERING_PROCESS

    elif step == 5:
        context.user_data["address"] = update.message.text

        client_data = {
            "name": context.user_data["name"],
            "cpf": context.user_data["cpf"],
            "phone_number": context.user_data["phone_number"],
            "city": context.user_data["city"],
            "address": context.user_data["address"],
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8001/clients/", json=client_data)

        if response.status_code == 200:
            await update.message.reply_text("Cadastro concluído! Obrigado pelas informações.")
        else:
            await update.message.reply_text("Houve um problema ao registrar o cadastro. Tente novamente mais tarde.")
        context.user_data.clear()
        return ConversationHandler.END
