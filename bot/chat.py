import httpx
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
    user_info = context.user_data.get('user_info', {})
    client_id = user_info['id']

    new_message_data = {
        "chat_id": 1,
        "message": message,
        "client_id": client_id,
    }

    print(new_message_data)

    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8001/messages/", json=new_message_data)
        print(response.json())
