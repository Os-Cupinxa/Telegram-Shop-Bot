# register.py
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

REGISTER = range(1)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Vamos iniciar o seu cadastro! Por favor, informe seu nome."
    )

    return ConversationHandler.END
