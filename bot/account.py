import re

import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def log_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Por favor, digite seu CPF para finalizar o pedido:")

    context.user_data['awaiting_cpf'] = True


async def check_user_by_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw_cpf = update.message.text
    cpf = re.sub(r'[.-]', '', raw_cpf)

    context.user_data['awaiting_cpf'] = False

    url = f"http://127.0.0.1:8001/clients/cpf/{cpf}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        client_data = response.json()
        context.user_data['user_info'] = client_data
        await show_user_info(update, context)
    else:
        from registering import start_registration
        await start_registration(update, context)


async def show_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = context.user_data.get('user_info', {})

    if not user_info:
        return

    cart_message = (
        f"**Dados do Cliente**\n\n"
        f"**Nome:** {user_info['name']}\n"
        f"**CPF:** {user_info['cpf']}\n"
        f"**Telefone:** {user_info['phone_number']}\n"
        f"**Cidade:** {user_info['city']}\n"
        f"**Endereço:** {user_info['address']}\n"
        f"**Status:** {'Ativo' if user_info['is_active'] else 'Inativo'}\n"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 Carrinho", callback_data="go_to-cart"),
         InlineKeyboardButton("📦 Catálogo", callback_data="go_to-catalogue")],
        [InlineKeyboardButton("🖊️ Editar Dados", callback_data="go_to-edit_user_info"),
         InlineKeyboardButton("🗂️️ Pedidos", callback_data="go_to-orders")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text(cart_message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.message.reply_text(cart_message, parse_mode='Markdown', reply_markup=reply_markup)
