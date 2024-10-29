import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from registering import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

AFTER_START, ALREADY_REGISTERED, AFTER_ALREADY_REGISTERED, CHECK_USER_BY_CPF, REGISTERING_PROCESS = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Sim", "Não"]]

    await update.message.reply_text(
        "Olá! Seja bem vindo a loja. "
        "Envie /cancelar para parar a conversa.\n\n"
        "Já possui um cadastro?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Sim ou não?"
        ),
    )

    return AFTER_START


async def after_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_response = update.message.text

    if user_response == "Sim":
        await update.message.reply_text("Certo! Por favor, informe seu CPF:")
        return ALREADY_REGISTERED
    elif user_response == "Não":
        context.registering_step = 0
        await registering_process(update, context)
        return REGISTERING_PROCESS
    else:
        await update.message.reply_text(
            "Por favor, responda apenas com 'Sim' ou 'Não'."
        )
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
            AFTER_START: [MessageHandler(filters.TEXT, after_start)],
            ALREADY_REGISTERED: [MessageHandler(filters.TEXT, already_registered)],
            CHECK_USER_BY_CPF: [MessageHandler(filters.TEXT, check_user_by_cpf)],
            REGISTERING_PROCESS: [MessageHandler(filters.TEXT | filters.CONTACT, registering_process)],
        },
        fallbacks=[CommandHandler("cancelar", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
