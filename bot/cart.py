from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


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
                cart.append({'product_id': product['id'], 'quantity': quantity, 'product': product})

            confirmation_message = (
                f"Adicionado ao carrinho:\n"
                f"**Produto:** {product['name']}\n"
                f"**Quantidade:** {quantity}\n"
                f"**Valor unitário:** R${unit_price:.2f}\n"
                f"**Total:** R${total_price:.2f}"
            )
            await update.message.reply_text(confirmation_message, parse_mode='Markdown')

            context.user_data['awaiting_quantity'] = False

            await show_cart(update, context)

        except ValueError:
            await update.message.reply_text("Por favor, insira um número válido.")

    else:
        await update.message.reply_text("Por favor, use o comando para adicionar um produto ao carrinho.")


async def show_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cart = context.user_data.get('cart', [])

    if not cart:
        if update.callback_query:
            await update.callback_query.message.reply_text("Seu carrinho está vazio.")
        else:
            await update.message.reply_text("Seu carrinho está vazio.")
        return

    total_cart_value = 0
    cart_message = "Seu carrinho contém:\n"

    for item in cart:
        product_id = item['product_id']
        quantity = item['quantity']
        product = item['product']

        if product:
            unit_price = product['price']
            total_price = unit_price * quantity
            total_cart_value += total_price
            cart_message += (
                f"**Produto:** {product['name']}\n"
                f"**Quantidade:** {quantity}\n"
                f"**Valor unitário:** R${unit_price:.2f}\n"
                f"**Total:** R${total_price:.2f}\n\n"
            )
        else:
            cart_message += f"Produto com ID {product_id} não encontrado.\n"

    cart_message += f"**Total do carrinho:** R${total_cart_value:.2f}"

    reply_keyboard = [
        [InlineKeyboardButton("🛒 Finalizar pedido", callback_data="c-finishPurchase"),
         InlineKeyboardButton("📦 Catálogo", callback_data="go_to-catalogue")]
    ]
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text(cart_message, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update.message.reply_text(cart_message, parse_mode='Markdown', reply_markup=reply_markup)
