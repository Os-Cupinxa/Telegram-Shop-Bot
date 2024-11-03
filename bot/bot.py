import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackQueryHandler,
)

from catalogue import *
from registering import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

AFTER_START, SHOW_CATALOGUE_CATEGORIES, ASK_FOR_QUANTITY, ALREADY_REGISTERED, AFTER_ALREADY_REGISTERED, CHECK_USER_BY_CPF, REGISTERING_PROCESS = range(
    7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        [InlineKeyboardButton("🛒 Carrinho", callback_data="carrinho"),
         InlineKeyboardButton("📦 Catálogo", callback_data="catalogo")]
    ]

    await update.message.reply_text(
        "Olá! Seja bem-vindo à loja. Como posso ajudar?",
        reply_markup=InlineKeyboardMarkup(reply_keyboard)
    )

    return AFTER_START


async def after_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "catalogo":
        await show_catalogue_categories(update, context)
        return SHOW_CATALOGUE_CATEGORIES
    elif query.data == "carrinho":
        await query.edit_message_text("Você clicou no carrinho!")
        return AFTER_START


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Usuário %s cancelou a conversa.", user.first_name)
    await update.message.reply_text(
        "Até mais!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("8007696885:AAEAB7ezULO2X2sAYGN23KbweAowb9XtsM8").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("iniciar", start)],
        states={
            AFTER_START: [CallbackQueryHandler(after_start)],
            SHOW_CATALOGUE_CATEGORIES: [MessageHandler(filters.TEXT, show_catalogue_categories)],
            ASK_FOR_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quantity)],
            ALREADY_REGISTERED: [MessageHandler(filters.TEXT, already_registered)],
            CHECK_USER_BY_CPF: [MessageHandler(filters.TEXT, check_user_by_cpf)],
            REGISTERING_PROCESS: [MessageHandler(filters.TEXT | filters.CONTACT, registering_process)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(show_products, pattern=r'show_products_\d+'))
    application.add_handler(CallbackQueryHandler(navigate_product, pattern=r'prev_product_\d+|next_product_\d+'))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
