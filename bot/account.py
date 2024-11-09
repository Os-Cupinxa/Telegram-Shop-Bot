import re

import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def log_in(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.message.reply_text("Por favor, digite seu CPF para finalizar o pedido:")

    context.user_data['awaiting_cpf_login'] = True


async def check_user_by_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw_cpf = update.message.text
    cpf = re.sub(r'[.-]', '', raw_cpf)

    context.user_data['awaiting_cpf_login'] = False

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
        f"👤 *Dados do Cliente*\n\n"
        f"✏️ *Nome:* {user_info['name']}\n"
        f"🆔 *CPF:* {user_info['cpf']}\n"
        f"📞 *Telefone:* {user_info['phone_number']}\n"
        f"🌆 *Cidade:* {user_info['city']}\n"
        f"🏠 *Endereço:* {user_info['address']}\n"
        f"🔓 *Status:* {'🟢 Ativo' if user_info['is_active'] else '🔴 Inativo'}\n"
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


async def choose_info_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("✏️ Nome", callback_data="go_to-edit_name"),
         InlineKeyboardButton("📞 Telefone", callback_data="go_to-edit_phone")],
        [InlineKeyboardButton("🌆 Cidade", callback_data="go_to-edit_city"),
         InlineKeyboardButton("🏠 Endereço", callback_data="go_to-edit_address")],
        [InlineKeyboardButton("🔙 Voltar ao Perfil", callback_data="go_to-profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.answer()
    await update.callback_query.message.reply_text("O que você gostaria de atualizar?", reply_markup=reply_markup)


async def edit_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["update_info_process"] = True
    context.user_data["awaiting_name_update"] = True
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Digite seu novo nome:")


async def edit_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["update_info_process"] = True
    context.user_data["awaiting_phone_update"] = True
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Digite seu novo telefone:")


async def edit_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["update_info_process"] = True
    context.user_data["awaiting_city_update"] = True
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Digite sua nova cidade:")


async def edit_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data["update_info_process"] = True
    context.user_data["awaiting_address_update"] = True
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("Digite seu novo endereço:")


async def update_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_name = update.message.text
    user_info = context.user_data.get('user_info', {})
    user_info['name'] = new_name
    context.user_data['user_info'] = user_info

    context.user_data['awaiting_name_update'] = False
    await update.message.reply_text(f"✔️ Nome atualizado para {new_name}.")
    await update_user_in_database(update, context)


async def update_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_phone = update.message.text
    user_info = context.user_data.get('user_info', {})
    user_info['phone_number'] = new_phone
    context.user_data['user_info'] = user_info

    context.user_data['awaiting_phone_update'] = False
    await update.message.reply_text(f"✔️ Telefone atualizado para {new_phone}.")
    await update_user_in_database(update, context)


async def update_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_city = update.message.text
    user_info = context.user_data.get('user_info', {})
    user_info['city'] = new_city
    context.user_data['user_info'] = user_info

    context.user_data['awaiting_city_update'] = False
    await update.message.reply_text(f"✔️ Cidade atualizada para {new_city}.")
    await update_user_in_database(update, context)


async def update_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    new_address = update.message.text
    user_info = context.user_data.get('user_info', {})
    user_info['address'] = new_address
    context.user_data['user_info'] = user_info

    context.user_data['awaiting_address_update'] = False
    await update.message.reply_text(f"✔️ Endereço atualizado para {new_address}.")
    await update_user_in_database(update, context)


async def update_user_in_database(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = context.user_data.get('user_info', {})

    if not user_info:
        await update.message.reply_text("❌ Não foi possível encontrar os dados do usuário para atualizar.")
        return

    payload = {
        "name": user_info.get('name'),
        "cpf": user_info.get('cpf'),
        "phone_number": user_info.get('phone_number'),
        "city": user_info.get('city'),
        "address": user_info.get('address'),
        "is_active": user_info.get('is_active', True)
    }

    client_id = user_info.get('id')

    url = f"http://127.0.0.1:8001/clients/?client_id={client_id}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=payload)

            if response.status_code == 200:
                context.user_data['user_info'] = response.json()
                await show_user_info(update, context)
            else:
                await update.message.reply_text(f"❌ Não foi possível salvar seus dados. Código de erro: {response.status_code}")
        except httpx.RequestError as e:
            await update.message.reply_text(f"❌ Erro ao tentar se comunicar com o servidor: {str(e)}")
