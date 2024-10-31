import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


async def show_catalogue_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    url = f"http://127.0.0.1:8001/categories/"

    async with httpx.AsyncClient() as categories:
        response = await categories.get(url)

    categories_data = response.json()

    print(categories_data)

    if response.status_code != 200:
        await update.message.reply_text("Erro ao buscar categorias.")
        return ConversationHandler.END

    if len(categories_data) > 0:
        categories_text = "\n".join([f"- {category['name']}" for category in categories_data])
        await update.callback_query.message.reply_text(f"Categorias:\n{categories_text}")
    else:
        await update.message.reply_text("Nenhuma categoria encontrada.")
        return ConversationHandler.END
