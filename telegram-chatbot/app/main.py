from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import asyncio

TELEGRAM_TOKEN = "8184388768:AAGVsj90ai9ua9jQoHzMSsR1oCkryD4TY7o"
RAG_SERVICE_URL = "http://rag-service:8082/query"
WAIT_SECONDS = 7


async def send_wait_message(chat_id, context):
    await asyncio.sleep(WAIT_SECONDS)
    await context.bot.send_message(chat_id=chat_id, text="Bancame, ya te respondo")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id

    wait_task = asyncio.create_task(send_wait_message(chat_id, context))

    try:
        loop = asyncio.get_event_loop()
        # Ejecutamos la request en un thread externo para no bloquear
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(RAG_SERVICE_URL, json={"message": user_message}, timeout=30)
        )

        wait_task.cancel()  # Si responde a tiempo, cancelamos el mensaje de espera

        data = response.json()
        final_answer = data.get("response", "Lo siento, no tengo respuesta.")
        await context.bot.send_message(chat_id=chat_id, text=final_answer)
    except Exception:
        wait_task.cancel()
        await context.bot.send_message(chat_id=chat_id, text="Ocurrió un error procesando tu consulta.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
