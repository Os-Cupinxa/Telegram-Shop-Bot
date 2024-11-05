import httpx
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


# async def registering_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     # Inicializando o passo se não existir
#     if "registering_step" not in context.user_data:
#         context.user_data["registering_step"] = 0
#
#     step = context.user_data["registering_step"]
#
#     if step == 0:
#         await update.message.reply_text("Vamos iniciar o seu cadastro! Por favor, informe seu nome.")
#         context.user_data["registering_step"] += 1
#         return REGISTERING_PROCESS
#
#     elif step == 1:
#         context.user_data["name"] = update.message.text
#         await update.message.reply_text("Ótimo! Agora, informe seu CPF.")
#         context.user_data["registering_step"] += 1
#         return REGISTERING_PROCESS
#
#     elif step == 2:
#         context.user_data["cpf"] = update.message.text
#
#         phone_button = KeyboardButton("Enviar meu número de telefone", request_contact=True)
#         reply_markup = ReplyKeyboardMarkup([[phone_button]], one_time_keyboard=True)
#         await update.message.reply_text("Por favor, compartilhe seu número de telefone.", reply_markup=reply_markup)
#
#         context.user_data["registering_step"] += 1
#         return REGISTERING_PROCESS
#
#     elif step == 3:
#         if update.message.contact:
#             context.user_data["phone_number"] = update.message.contact.phone_number
#         else:
#             context.user_data["phone_number"] = update.message.text
#
#         await update.message.reply_text("Quase lá! Agora, informe sua cidade.")
#         context.user_data["registering_step"] += 1
#         return REGISTERING_PROCESS
#
#     elif step == 4:
#         context.user_data["city"] = update.message.text
#         await update.message.reply_text("Por último, informe seu endereço.")
#         context.user_data["registering_step"] += 1
#         return REGISTERING_PROCESS
#
#     elif step == 5:
#         context.user_data["address"] = update.message.text
#
#         client_data = {
#             "name": context.user_data["name"],
#             "cpf": context.user_data["cpf"],
#             "phone_number": context.user_data["phone_number"],
#             "city": context.user_data["city"],
#             "address": context.user_data["address"],
#         }
#
#         async with httpx.AsyncClient() as client:
#             response = await client.post("http://127.0.0.1:8001/clients/", json=client_data)
#
#         if response.status_code == 200:
#             await update.message.reply_text("Cadastro concluído! Obrigado pelas informações.")
#         else:
#             await update.message.reply_text("Houve um problema ao registrar o cadastro. Tente novamente mais tarde.")
#         context.user_data.clear()
#         return ConversationHandler.END
