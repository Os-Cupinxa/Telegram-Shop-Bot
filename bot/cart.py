from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split("-")[1])
    context.user_data['current_product_id'] = product_id

    await query.message.reply_text("Por favor, digite a quantidade de itens que deseja adicionar ao carrinho:")

    context.user_data['awaiting_quantity'] = True


async def handle_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_quantity'):
        try:
            quantity = int(update.message.text)

            if quantity <= 0:
                await update.message.reply_text("Por favor, insira uma quantidade válida (maior que 0).")
                return

            current_index = context.user_data.get('current_product_index', 0)
            products = context.user_data.get('products', [])
            product = products[current_index]

            unit_price = product['price']
            total_price = unit_price * quantity

            if 'cart' not in context.user_data:
                context.user_data['cart'] = []

            cart = context.user_data['cart']

            for item in cart:
                if item['product_id'] == product['id']:
                    item['quantity'] += quantity
                    break
            else:
                cart.append({'product_id': product['id'], 'quantity': quantity})

            confirmation_message = (
                f"Adicionado ao carrinho:\n"
                f"**Produto:** {product['name']}\n"
                f"**Quantidade:** {quantity}\n"
                f"**Valor unitário:** R${unit_price:.2f}\n"
                f"**Total:** R${total_price:.2f}"
            )
            await update.message.reply_text(confirmation_message, parse_mode='Markdown')

            context.user_data['awaiting_quantity'] = False

        except ValueError:
            await update.message.reply_text("Por favor, insira um número válido.")

    else:
        await update.message.reply_text("Por favor, use o comando para adicionar um produto ao carrinho.")
