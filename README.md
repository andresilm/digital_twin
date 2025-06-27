# Digital Twin

This project contains three Docker services:

- `telegram-chatbot`: the bot that interacts with Telegram  
- `rag-service`: retrieval augmented generation (RAG) service for queries  
- `llm-service`: service that handles the language model (LLM)  

---

## Requirements

- Docker and Docker Compose installed  
- Bash shell to run the `manage.sh` script  
- A chatbot created in Telegram and its token loaded in environment variable "TELEGRAM_TOKEN" 
  or put in telegram-chatbot/app/main.py file
- A key for Google Gemini, loaded in environment variable "MY_GOOGLE_API_KEY" or 
  put in llm-service/app/google_gemini/llm.py file
---

## Project structure

```plaintext
.
├── docker-compose.yml
├── manage.sh
├── telegram-chatbot/
├── rag-service/
└── llm-service/
```

---

## Usage

### Build Docker images

```bash
./manage.sh build
```

### Start all services

- In foreground (for development/debugging):

```bash
./manage.sh up
```

- In detached mode (daemon):

```bash
./manage.sh up-detached
```

### Stop services

```bash
./manage.sh down
```

### View logs of all services

```bash
./manage.sh logs
```

### Clean everything (containers, images, volumes)

```bash
./manage.sh clean
```

---

## Additional details

- The folders `telegram-chatbot`, `rag-service` and `llm-service` each contain their respective code and Dockerfile.  
- Services expose the following ports:
  - `telegram-chatbot`: 8081  
  - `rag-service`: 8082  
  - `llm-service`: 8083  
- `telegram-chatbot` depends on `rag-service`, which depends on `llm-service`.  

---


