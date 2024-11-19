import asyncio
import logging

import nest_asyncio
from telegram import ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters, CallbackQueryHandler,
)

from account import log_in, check_user_by_cpf, choose_info_to_edit, show_user_info, update_name, update_phone, \
    update_city, update_address, edit_name, edit_phone, edit_city, edit_address
from env_config import TELEGRAM_BOT_TOKEN
from cart import show_cart, handle_quantity, add_to_cart, prompt_remove_item, confirm_remove_from_cart, \
    confirm_clean_cart
from catalogue import show_catalogue_categories, get_products, navigate_product
from chat import start_chat, save_message
from checkout import checkout, confirm_order
from orders import get_orders, navigate_order, get_order_details
from registering import process_name, process_phone, process_city, process_address

nest_asyncio.apply()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = context.user_data.get('user_info', {})

    if user_info:
        reply_keyboard = [
            [
                InlineKeyboardButton("🛒 Carrinho", callback_data=f"go_to-cart"),
                InlineKeyboardButton("📦 Catálogo", callback_data=f"go_to-catalogue"),
                InlineKeyboardButton("👤 Ver Conta", callback_data=f"go_to-profile")
            ]
        ]
        start_text = (
            f"Olá, {user_info.get('name', 'Usuário')}! Seja bem-vindo de volta à loja. 😊\n"
            "Como posso ajudar hoje?\n"
            "Digite /ajuda para exibir a lista de comandos \n"
            "ou selecione uma das opções abaixo.\n"
        )
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton("🛒 Carrinho", callback_data=f"go_to-cart"),
                InlineKeyboardButton("📦 Catálogo", callback_data=f"go_to-catalogue"),
                InlineKeyboardButton("🙋 Efetuar Login", callback_data=f"go_to-login")
            ]
        ]
        start_text = (
            "Olá! Seja bem-vindo à loja. 😊\n"
            "Você não está logado no momento.\n"
            "Digite /ajuda para exibir a lista de comandos \n"
            "ou selecione uma das opções abaixo.\n"
        )

    await update.message.reply_text(
        start_text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
    )


async def go_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    page = query.data.split("-")[1]

    if page == "catalogue":
        await show_catalogue_categories(update, context)

    elif page == "cart":
        await show_cart(update, context)

    elif page == "profile":
        await show_user_info(update, context)

    elif page == "orders":
        await get_orders(update, context)

    elif page == "login":
        await log_in(update, context)

    elif page == "edit_user_info":
        await choose_info_to_edit(update, context)

    elif page == "edit_name":
        await edit_name(update, context)

    elif page == "edit_phone":
        await edit_phone(update, context)

    elif page == "edit_city":
        await edit_city(update, context)

    elif page == "edit_address":
        await edit_address(update, context)

    elif page == "checkout":
        user_info = context.user_data.get('user_info', {})
        context.user_data['is_checking_out'] = True
        if not user_info:
            await log_in(update, context)
        else:
            await checkout(update, context)

    elif page == "confirm_checkout":
        await confirm_order(update, context)


async def handle_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('registering_process', False):
        if context.user_data.get("awaiting_name"):
            await process_name(update, context)
        elif context.user_data.get("awaiting_phone"):
            await process_phone(update, context)
        elif context.user_data.get("awaiting_city"):
            await process_city(update, context)
        elif context.user_data.get("awaiting_address"):
            await process_address(update, context)

    if context.user_data.get('update_info_process', False):
        if context.user_data.get("awaiting_name_update"):
            await update_name(update, context)
        elif context.user_data.get("awaiting_phone_update"):
            await update_phone(update, context)
        elif context.user_data.get("awaiting_city_update"):
            await update_city(update, context)
        elif context.user_data.get("awaiting_address_update"):
            await update_address(update, context)

    elif context.user_data.get('awaiting_cpf_login', False):
        await check_user_by_cpf(update, context)

    elif context.user_data.get('awaiting_quantity', False):
        await handle_quantity(update, context)

    elif context.user_data.get('awaiting_chat_inputs', False):
        await save_message(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    await update.message.reply_text(
        "Até mais!", reply_markup=ReplyKeyboardRemove()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "📋 *Lista de Comandos Disponíveis:*\n\n"
        "🔹 /iniciar - Iniciar a conversa\n"
        "🔹 /cancelar - Cancelar a conversa\n"
        "🔹 /carrinho - Ver seu carrinho de compras\n"
        "🔹 /catalogo - Exibir o catálogo da loja\n"
        "🔹 /chat - Iniciar conversa com atendente\n"
        "🔹 /conta - Ver informações da sua conta\n"
        "🔹 /ajuda - Mostrar esta lista de comandos\n"
        "\n💬 *Se precisar de ajuda adicional, estou à disposição!*"
    )

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def main() -> None:
    # SOCKET IS DISABLED FOR NOW BECAUSE IT'S NOT WORKING CORRECTLY IN THE BOT. ALSO FOR NOW THERE IS NO NEED TO USE IT
    # from socket_config import connect_to_backend
    # await connect_to_backend()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("iniciar", start))
    application.add_handler(CommandHandler("cancelar", cancel))
    application.add_handler(CommandHandler("carrinho", show_cart))
    application.add_handler(CommandHandler("catalogo", show_catalogue_categories))
    application.add_handler(CommandHandler("chat", start_chat))
    application.add_handler(CommandHandler("conta", show_user_info))
    application.add_handler(CommandHandler("ajuda", help_command))

    application.add_handler(CallbackQueryHandler(go_to, pattern=r'go_to-.*'))
    application.add_handler(CallbackQueryHandler(get_products, pattern=r'show_products-.*'))
    application.add_handler(CallbackQueryHandler(navigate_product, pattern=r'prev_product|next_product'))
    application.add_handler(CallbackQueryHandler(navigate_order, pattern=r'prev_order|next_order'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern=r'add_to_cart-.*'))
    application.add_handler(CallbackQueryHandler(get_order_details, pattern=r'see_order_details-.*'))
    application.add_handler(CallbackQueryHandler(prompt_remove_item, pattern=r'prompt_remove_item'))
    application.add_handler(CallbackQueryHandler(confirm_remove_from_cart, pattern=r'confirm_remove_item-.*'))
    application.add_handler(CallbackQueryHandler(confirm_clean_cart, pattern=r'confirm_clean_cart'))

    application.add_handler(MessageHandler((filters.TEXT | filters.CONTACT) & ~filters.COMMAND, handle_input))

    await application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    asyncio.run(main())
