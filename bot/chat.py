from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = context.user_data.get('user_info', {})

    if not user_info:
        reply_keyboard = [InlineKeyboardButton("🙋 Efetuar Login", callback_data=f"go_to-login")]

        await update.message.reply_text(
            "Você não está logado!",
            reply_markup=InlineKeyboardMarkup([reply_keyboard])
        )
        return

    context.user_data["awaiting_chat_inputs"] = True
    await update.message.reply_text("Conversa iniciada")


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    print(message)
