from telegram import Update
from telegram.ext import ContextTypes
import httpx


async def checkout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cart = context.user_data.get('cart', [])
    user_info = context.user_data.get('user_info', {})

    cart_items = [{'product_id': item['product_id'], 'quantity': item['quantity']} for item in cart]

    order_data = {
        "client_id": user_info['id'],
        "status": "pending",
        "amount": 1,
        "items": cart_items
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8001/orders/", json=order_data)

    if response.status_code == 200:
        order_response = response.json()

        message = (
            f"🎉 *Pedido criado com sucesso!*\n\n"
            f"🆔 *Número do Pedido*: {order_response['id']}\n"
            f"📅 *Data do Pedido*: {order_response['created_date']}\n"
            f"💵 *Total*: R$ {order_response['amount']}\n"
            f"📦 *Status*: {order_response['status']}\n\n"
        )

        if update.callback_query:
            await update.callback_query.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode="Markdown")
    else:
        error_message = (
            f"❌ *Erro ao criar pedido!*\n\n"
            f"Por favor tente novamente mais tarde!\n"
        )

        if update.callback_query:
            await update.callback_query.message.reply_text(error_message, parse_mode='Markdown')
        else:
            await update.message.reply_text(error_message, parse_mode="Markdown")
