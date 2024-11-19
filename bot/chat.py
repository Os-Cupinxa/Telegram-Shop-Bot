import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from env_config import SERVER_URL


async def start_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    is_chat_active = context.user_data.get('awaiting_chat_inputs', {})

    if is_chat_active:
        context.user_data["awaiting_chat_inputs"] = False
        await update.message.reply_text(
            "✅ *Conversa com atendente encerrada!*",
            parse_mode="Markdown"
        )
        return

    user_info = context.user_data.get('user_info', {})

    if not user_info:
        reply_keyboard = [InlineKeyboardButton("🙋 Efetuar Login", callback_data=f"go_to-login")]

        await update.message.reply_text(
            "Você não está logado!",
            reply_markup=InlineKeyboardMarkup([reply_keyboard])
        )
        return

    context.user_data["awaiting_chat_inputs"] = True
    await update.message.reply_text(
        "✅ *Conversa com atendente iniciada!*\n\n"
        "📩 Agora você pode enviar suas mensagens.\n"
        "❗ Para encerrar a conversa, basta enviar o comando */chat* novamente.",
        parse_mode="Markdown"
    )


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text
    user_info = context.user_data.get('user_info', {})
    client_id = user_info['id']
    chat_id = update.message.chat.id

    new_message_data = {
        "chat_id": chat_id,
        "message": message,
        "client_id": client_id,
    }

    async with httpx.AsyncClient() as client:
        await client.post(f"{SERVER_URL}/messages/", json=new_message_data)
