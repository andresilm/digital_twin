FROM python:3.10-slim
WORKDIR /app
COPY app /app
RUN pip install fastapi openai uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8083"]