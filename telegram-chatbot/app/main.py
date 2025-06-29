import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
import asyncio
import os


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")

RAG_SERVICE_URL = "http://rag-service:8082/query"
WAIT_SECONDS = 7


async def send_wait_message(chat_id, context):
    """
    Wait WAIT_SECONDS seconds then send a waiting message to the Telegram chat.

    Args:
        chat_id (int): Telegram chat ID to send the message to.
        context: Bot context to send messages.
    """
    await asyncio.sleep(WAIT_SECONDS)
    await context.bot.send_message(chat_id=chat_id, text="Esperame, ya te respondo...")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        logger.warning("Received update without text message: %s", update)
        return

    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.debug(f"Received message from chat_id={chat_id}: {user_message}")

    wait_task = asyncio.create_task(send_wait_message(chat_id, context))

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: requests.post(RAG_SERVICE_URL, json={"message": user_message}, timeout=30)
        )

        wait_task.cancel()

        data = response.json()
        final_answer = data.get("response", "Sorry, I don't have an answer.")

        logger.debug(f"Sending response to chat_id={chat_id}: {final_answer}")
        await context.bot.send_message(chat_id=chat_id, text=final_answer)
    except Exception as e:
        wait_task.cancel()
        logger.error(f"Error processing request: {e}")
        await context.bot.send_message(chat_id=chat_id, text="An error occurred while processing your request.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
