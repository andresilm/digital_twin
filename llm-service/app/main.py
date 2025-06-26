from fastapi import FastAPI
from pydantic import BaseModel
from google_gemini.llm import GeminiLLM

app = FastAPI()
gemini_llm = GeminiLLM()


class CompletionRequest(BaseModel):
    user_input: str
    base_profile: str
    context: str


@app.post("/complete")
async def complete(req: CompletionRequest):
    generated_content = gemini_llm.generate_content(user_input=req.user_input, document=req.context,
                                                    base_profile=req.base_profile)
    return {"response": generated_content}
