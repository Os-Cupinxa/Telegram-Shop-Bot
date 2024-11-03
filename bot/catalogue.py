import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


async def show_catalogue_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    url = "http://127.0.0.1:8001/categories/"

    async with httpx.AsyncClient() as categories:
        response = await categories.get(url)

    categories_data = response.json()

    print(categories_data)

    if response.status_code != 200:
        await update.message.reply_text("Erro ao buscar categorias.")
        return ConversationHandler.END

    if len(categories_data) > 0:
        keyboard = [
            [InlineKeyboardButton(category['name'], callback_data=f"show_products_{category['id']}")]
            for category in categories_data
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Categorias:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Nenhuma categoria encontrada.")
        return ConversationHandler.END


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    category_id = query.data.split("_")[2]
    url = f"http://127.0.0.1:8001/categories/{category_id}/products"

    async with httpx.AsyncClient() as products_client:
        response = await products_client.get(url)

    products_data = response.json()

    if response.status_code != 200:
        await query.message.reply_text("Erro ao buscar produtos.")
        return

    context.user_data['products'] = products_data
    context.user_data['current_product_index'] = 0

    await display_product(update, context)


async def display_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    products = context.user_data.get('products', [])
    current_index = context.user_data.get('current_product_index', 0)

    if not products:
        await update.message.reply_text("Nenhum produto encontrado.")
        return

    product = products[current_index]

    product_text = (
        f"**Nome:** {product['name']}\n"
        f"**Descrição:** {product['description']}\n"
        f"**Preço:** R${product['price']:.2f}\n"
        f"[Imagem]({product['photo_url']})"
    )

    keyboard = []

    if current_index > 0:
        previous_button = InlineKeyboardButton("Anterior", callback_data=f"prev_product_{current_index}")
        keyboard.append(previous_button)

    if current_index < len(products) - 1:
        next_button = InlineKeyboardButton("Próximo", callback_data=f"next_product_{current_index}")
        keyboard.append(next_button)

    if keyboard:
        reply_markup = InlineKeyboardMarkup([keyboard])
    else:
        reply_markup = None

    await update.callback_query.message.reply_text(product_text, reply_markup=reply_markup, parse_mode='Markdown')


async def navigate_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    products = context.user_data.get('products', [])
    current_index = context.user_data.get('current_product_index', 0)

    if "prev_product" in query.data:
        current_index -= 1
    elif "next_product" in query.data:
        current_index += 1

    context.user_data['current_product_index'] = current_index

    await display_product(update, context)
