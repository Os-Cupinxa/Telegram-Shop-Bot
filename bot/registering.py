import re

import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from env_config import SERVER_URL


async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    registration_message = (
        f"*Você ainda não possui uma conta.*\n\n"
        f"Vamos iniciar o seu cadastro! Por favor, *informe seu nome:*"
    )

    context.user_data["update_info_process"] = False
    context.user_data["registering_process"] = True
    context.user_data["awaiting_name"] = True
    await update.message.reply_text(registration_message, parse_mode='Markdown')


async def process_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    name = update.message.text

    if re.search(r'\d', name):
        await update.message.reply_text("O nome não deve conter números. Por favor, insira um nome válido.")
        return

    context.user_data["new_user"]["name"] = name
    context.user_data["awaiting_name"] = False
    context.user_data["awaiting_phone"] = True

    contact_button = KeyboardButton("Compartilhar meu número de telefone", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Por favor, compartilhe *seu número de telefone:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


async def process_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.contact:
        phone_number = update.message.contact.phone_number
    else:
        phone_number = update.message.text

    context.user_data["new_user"]["phone_number"] = phone_number
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
    chat_id = update.message.chat.id

    new_user_data = {
        "name": context.user_data["new_user"]["name"],
        "cpf": context.user_data["new_user"]["cpf"],
        "phone_number": context.user_data["new_user"]["phone_number"],
        "city": context.user_data["new_user"]["city"],
        "address": context.user_data["new_user"]["address"],
        "chat_id": chat_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVER_URL}/clients/", json=new_user_data)

    if response.status_code == 200:
        client_data = response.json()
        context.user_data['user_info'] = client_data
        await update.message.reply_text("Cadastro concluído! Obrigado pelas informações.")
        from account import show_user_info
        await show_user_info(update, context)
    else:
        await update.message.reply_text("Houve um problema ao registrar o cadastro. Tente novamente mais tarde.")

    context.user_data["new_user"] = {}
