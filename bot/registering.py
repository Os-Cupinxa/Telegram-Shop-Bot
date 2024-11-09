import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    registration_message = (
        f"*Você ainda não possui uma conta.*\n\n"
        f"Vamos iniciar o seu cadastro! Por favor, *informe seu nome:*"
    )

    context.user_data["update_info_process"] = False
    context.user_data["registering_process"] = True
    context.user_data["awaiting_name"] = True
    context.user_data["new_user"] = {}
    await update.message.reply_text(registration_message, parse_mode='Markdown')


async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["new_user"]["name"] = update.message.text
    context.user_data["awaiting_name"] = False
    context.user_data["awaiting_cpf"] = True
    await update.message.reply_text("Ótimo! Agora, *informe seu CPF:*", parse_mode='Markdown')


async def process_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["new_user"]["cpf"] = update.message.text
    context.user_data["awaiting_cpf"] = False
    context.user_data["awaiting_phone"] = True
    await update.message.reply_text("Por favor, compartilhe *seu número de telefone:*", parse_mode='Markdown')


async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["new_user"]["phone_number"] = update.message.text
    context.user_data["awaiting_phone"] = False
    context.user_data["awaiting_city"] = True
    await update.message.reply_text("Quase lá! Agora, *informe sua cidade:*", parse_mode='Markdown')


async def process_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["new_user"]["city"] = update.message.text
    context.user_data["awaiting_city"] = False
    context.user_data["awaiting_address"] = True
    await update.message.reply_text("Por último, *informe seu endereço.*", parse_mode='Markdown')


async def process_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["new_user"]["address"] = update.message.text
    context.user_data["awaiting_address"] = False
    context.user_data["registering_process"] = False

    new_user_data = {
        "name": context.user_data["new_user"]["name"],
        "cpf": context.user_data["new_user"]["cpf"],
        "phone_number": context.user_data["new_user"]["phone_number"],
        "city": context.user_data["new_user"]["city"],
        "address": context.user_data["new_user"]["address"],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8001/clients/", json=new_user_data)

    if response.status_code == 200:
        client_data = response.json()
        context.user_data['user_info'] = client_data
        await update.message.reply_text("Cadastro concluído! Obrigado pelas informações.")
        from account import show_user_info
        await show_user_info(update, context)
    else:
        await update.message.reply_text("Houve um problema ao registrar o cadastro. Tente novamente mais tarde.")

    context.user_data.clear()
