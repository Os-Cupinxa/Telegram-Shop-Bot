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
from cart import *
from registering import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [
        [InlineKeyboardButton("🛒 Carrinho", callback_data=f"go_to-cart"),
         InlineKeyboardButton("📦 Catálogo", callback_data=f"go_to-catalogue")]
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

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quantity))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
