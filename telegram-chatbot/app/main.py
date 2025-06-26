from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
RAG_SERVICE_URL = "http://rag-service:8082/query"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    await update.message.reply_text("Estoy procesando tu consulta, dame unos segundos...")

    try:
        response = requests.post(RAG_SERVICE_URL, json={"message": user_message}, timeout=30)
        data = response.json()
        final_answer = data.get("response", "Lo siento, no tengo respuesta.")
        await context.bot.send_message(chat_id=chat_id, text=final_answer)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text="Ocurrió un error procesando tu consulta.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
