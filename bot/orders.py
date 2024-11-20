from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import httpx

from env_config import SERVER_URL
from utils import format_date


async def get_orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    client_id = context.user_data.get('user_info', {}).get('id')

    if not client_id:
        await query.message.reply_text("ID do cliente não encontrado.")
        return

    url = f"{SERVER_URL}/orders/client/{client_id}"

    async with httpx.AsyncClient() as orders_client:
        response = await orders_client.get(url)

    if response.status_code != 200:
        await query.message.reply_text("Erro ao buscar pedidos.")
        return

    orders_data = response.json()

    context.user_data['orders'] = orders_data
    context.user_data['current_order_index'] = 0

    await display_order(query, context)


async def display_order(query: Update.callback_query, context: ContextTypes.DEFAULT_TYPE) -> None:
    orders = context.user_data.get('orders', [])
    current_index = context.user_data.get('current_order_index', 0)

    if not orders:
        await query.message.reply_text("Nenhum pedido encontrado.")
        return

    order = orders[current_index]
    formated_date = format_date(order['created_date'])

    order_text = (
        f"🆔 *Número do Pedido*: {order['id']}\n"
        f"📅 *Data do Pedido*: {formated_date}\n"
        f"💵 *Total*: R$ {order['amount']:.2f}\n"
        f"📦 *Status*: {order['status']}\n\n"
    )

    navigation_buttons = []
    if current_index > 0:
        previous_button = InlineKeyboardButton("⬅️ Pedido Anterior", callback_data=f"prev_order")
        navigation_buttons.append(previous_button)

    if current_index < len(orders) - 1:
        next_button = InlineKeyboardButton("Próximo Pedido ➡️", callback_data=f"next_order")
        navigation_buttons.append(next_button)

    see_order_details_button = InlineKeyboardButton("🔎 Ver Detalhes", callback_data=f"see_order_details-{order['id']}")
    profile_button = InlineKeyboardButton("🔙 Voltar", callback_data=f"go_to-profile")

    keyboard = []
    if navigation_buttons:
        keyboard.append(navigation_buttons)
    keyboard.append([see_order_details_button, profile_button])

    reply_markup = InlineKeyboardMarkup(keyboard)

    # TODO VER ERRO QUE OCORRE AQUI AO TROCAR O PEDIDO
    await query.edit_message_text(order_text, reply_markup=reply_markup, parse_mode='Markdown')


async def navigate_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    current_index = context.user_data.get('current_order_index', 0)

    if "prev_order" in query.data:
        current_index -= 1
    elif "next_order" in query.data:
        current_index += 1

    context.user_data['current_order_index'] = current_index

    await display_order(update.callback_query, context)
    await display_order(query, context)


async def get_order_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    orders = context.user_data.get('orders', [])
    current_index = context.user_data.get('current_order_index', 0)
    order_id = orders[current_index]['id'] if orders else None

    if not order_id:
        await query.message.reply_text("Pedido não encontrado.")
        return

    url = f"{SERVER_URL}/orders/items/{order_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        await query.message.reply_text("Erro ao buscar detalhes do pedido.")
        return

    items_data = response.json()

    order = orders[current_index]
    formated_date = format_date(order['created_date'])

    order_text = (
        f"🆔 *Número do Pedido*: {order['id']}\n"
        f"📅 *Data do Pedido*: {formated_date}\n"
        f"💵 *Total*: R$ {order['amount']:.2f}\n"
        f"📦 *Status*: {order['status']}\n\n"
        "📜 *Itens do Pedido:*\n"
        f"--------------------------------------------------\n"
    )

    for item in items_data:
        product = item['product']
        quantity = item['quantity']
        unit_price = product['price']
        total_price = unit_price * quantity

        order_text += (
            f"🛍️ *Produto:* {product['name']}\n"
            f"🔢 *Quantidade:* {quantity}\n"
            f"💵 *Valor unitário:* R$ {unit_price:.2f}\n"
            f"💰 *Total:* R$ {total_price:.2f}\n"
            f"--------------------------------------------------\n"
        )

    back_button = InlineKeyboardButton("🔙 Voltar aos Pedidos", callback_data="go_to-orders")
    keyboard = [[back_button]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(order_text, reply_markup=reply_markup, parse_mode='Markdown')
