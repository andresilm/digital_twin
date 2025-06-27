from fastapi import FastAPI
from google_gemini.llm import GeminiLLM
from models import CompletionRequest

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """
    FastAPI startup event handler.

    Initializes and stores the GeminiLLM instance in the application state
    so it can be reused across requests without recreating it.
    """
    app.state.gemini_llm = GeminiLLM()


@app.post("/complete")
async def complete(req: CompletionRequest):
    """
    Endpoint to generate a completion response using GeminiLLM.

    Args:
        req (CompletionRequest): Request body containing the user input,
                                 context document, and base profile.

    Returns:
        dict: A dictionary with the key 'response' containing the generated text.

    Behavior:
        - Retrieves the GeminiLLM instance from the app state.
        - Calls the generate_content method passing user input, context, and base profile.
        - Returns the generated response as JSON.
    """
    gemini_llm = app.state.gemini_llm
    generated_content = gemini_llm.generate_content(
        user_input=req.user_input,
        document=req.context,
        base_profile=req.base_profile
    )
    return {"response": generated_content}
