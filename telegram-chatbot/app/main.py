import requests
import time
import threading

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GET_UPDATES_URL = f"{TELEGRAM_API_URL}/getUpdates"
SEND_MESSAGE_URL = f"{TELEGRAM_API_URL}/sendMessage"
RAG_SERVICE_URL = "http://rag-service:8082/query"


def send_message(chat_id, text):
    requests.post(SEND_MESSAGE_URL, json={"chat_id": chat_id, "text": text})


def process_message(chat_id, message):
    try:
        response = requests.post(RAG_SERVICE_URL, json={"message": message}, timeout=30)
        data = response.json()
        final_answer = data.get("response", "Lo siento, no tengo respuesta.")
        send_message(chat_id, final_answer)
    except Exception as e:
        send_message(chat_id, "Ocurrió un error procesando tu consulta.")


def poll_telegram():
    last_update_id = None
    while True:
        response = requests.get(GET_UPDATES_URL, timeout=10)
        data = response.json()
        for update in data.get("result", []):
            update_id = update["update_id"]
            message = update.get("message", {}).get("text")
            chat_id = update.get("message", {}).get("chat", {}).get("id")

            if update_id != last_update_id and message:
                last_update_id = update_id
                # Response immediately
                send_message(chat_id, "Estoy procesando tu consulta, dame unos segundos...")
                # Process in background
                threading.Thread(target=process_message, args=(chat_id, message)).start()
        time.sleep(2)


if __name__ == "__main__":
    poll_telegram()
