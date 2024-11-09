import logging

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
from cart import show_cart, handle_quantity, add_to_cart, prompt_remove_item, confirm_remove_from_cart
from catalogue import show_catalogue_categories, get_products, navigate_product
from checkout import checkout, confirm_order
from registering import process_name, process_cpf, process_phone, process_city, process_address

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [
        [InlineKeyboardButton("🛒 Carrinho", callback_data=f"go_to-cart"),
         InlineKeyboardButton("📦 Catálogo", callback_data=f"go_to-catalogue"),
         InlineKeyboardButton("🙋 Efetuar Login", callback_data=f"go_to-login")]
    ]

    await update.message.reply_text(
        "Olá! Seja bem-vindo à loja. Como posso ajudar?",
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
    )


async def go_to(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    page = query.data.split("-")[1]

    if page == "catalogue":
        await show_catalogue_categories(query, context)

    elif page == "cart":
        await show_cart(update, context)

    elif page == "profile":
        await show_user_info(update, context)

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
        elif context.user_data.get("awaiting_cpf"):
            await process_cpf(update, context)
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


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Até mais!", reply_markup=ReplyKeyboardRemove()
    )


def main() -> None:
    application = Application.builder().token("8007696885:AAEAB7ezULO2X2sAYGN23KbweAowb9XtsM8").build()

    application.add_handler(CommandHandler("iniciar", start))
    application.add_handler(CommandHandler("cancelar", cancel))
    application.add_handler(CommandHandler("carrinho", show_cart))

    application.add_handler(CallbackQueryHandler(go_to, pattern=r'go_to-.*'))
    application.add_handler(CallbackQueryHandler(get_products, pattern=r'show_products-.*'))
    application.add_handler(CallbackQueryHandler(navigate_product, pattern=r'prev_product|next_product'))
    application.add_handler(CallbackQueryHandler(add_to_cart, pattern=r'add_to_cart-.*'))
    application.add_handler(CallbackQueryHandler(prompt_remove_item, pattern=r'prompt_remove_item'))
    application.add_handler(CallbackQueryHandler(confirm_remove_from_cart, pattern=r'confirm_remove_item-.*'))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_input))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
