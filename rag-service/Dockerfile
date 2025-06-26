FROM python:3.10-slim
WORKDIR /app
COPY app /app
COPY data_ingestion /app/data_ingestion
RUN pip install fastapi uvicorn langchain openai
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]