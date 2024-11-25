import httpx
import requests
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes, ConversationHandler

from env_config import SERVER_URL


async def show_catalogue_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = f"{SERVER_URL}/categories/"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    categories_data = response.json()

    if response.status_code != 200:
        error_message = "Erro ao buscar categorias. Por favor tente mais tarde!"

        if update.callback_query:
            await update.callback_query.message.reply_text(error_message)
        else:
            await update.message.reply_text(error_message)
        return

    if len(categories_data) > 0:
        keyboard = [
            [InlineKeyboardButton(f"{category['emoji']} {category['name']}",
                                  callback_data=f"show_products-{category['id']}")]
            for category in categories_data
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.message.reply_text("Selecione a categoria:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("Selecione a categoria:", reply_markup=reply_markup)
    else:
        if update.callback_query:
            await update.callback_query.message.reply_text("Sinto muito, nenhuma categoria encontrada.")
        else:
            await update.message.reply_text("Sinto muito, nenhuma categoria encontrada.")


async def get_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    category_id = query.data.split("-")[1]

    url = f"{SERVER_URL}/categories/{category_id}/products"

    async with httpx.AsyncClient() as products_client:
        response = await products_client.get(url)

    if response.status_code != 200:
        await query.message.reply_text("Erro ao buscar produtos.")
        return

    products_data = response.json()

    context.user_data['products'] = products_data
    context.user_data['current_product_index'] = 0

    await display_product(query, context)


async def display_product(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE) -> None:
    products = context.user_data.get('products', [])
    current_index = context.user_data.get('current_product_index', 0)

    if not products:
        await query.message.reply_text("Nenhum produto encontrado.")
        return

    product = products[current_index]

    try:
        response = requests.get(product['photo_url'], timeout=10)
        response.raise_for_status()
        image = BytesIO(response.content)
        image.name = "product.jpg"
    except requests.RequestException as e:
        await query.message.reply_text(f"Erro ao carregar a imagem: {e}")
        return

    product_text = (
        f"📦 *Nome:* {product['name']}\n"
        f"📝 *Descrição:* {product['description']}\n"
        f"💵 *Preço:* R$ {product['price']:.2f}\n"
    )

    navigation_buttons = []
    if current_index > 0:
        previous_button = InlineKeyboardButton("⬅️ Produto Anterior", callback_data=f"prev_product")
        navigation_buttons.append(previous_button)

    if current_index < len(products) - 1:
        next_button = InlineKeyboardButton("Próximo Produto ➡️", callback_data=f"next_product")
        navigation_buttons.append(next_button)

    add_to_cart_button = InlineKeyboardButton("➕ Adicionar ao Carrinho", callback_data=f"add_to_cart-{product['id']}")
    cart_button = InlineKeyboardButton("🛒 Carrinho", callback_data=f"go_to-cart")

    keyboard = []
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    keyboard.append([add_to_cart_button, cart_button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.delete()
    await query.message.reply_photo(
        photo=InputFile(image),
        caption=product_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def navigate_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    current_index = context.user_data.get('current_product_index', 0)

    if "prev_product" in query.data:
        current_index -= 1
    elif "next_product" in query.data:
        current_index += 1

    context.user_data['current_product_index'] = current_index

    await display_product(query, context)
