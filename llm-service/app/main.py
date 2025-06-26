from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class CompletionRequest(BaseModel):
    user_input: str
    context: str

@app.post("/complete")
async def complete(req: CompletionRequest):
    prompt = f"Context: {req.context}\nUser: {req.user_input}\nAnswer:"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Only answer questions relevant to the user's experience."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"response": completion.choices[0].message["content"]}