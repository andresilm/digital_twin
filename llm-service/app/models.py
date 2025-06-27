from pydantic import BaseModel


class CompletionRequest(BaseModel):
    user_input: str
    base_profile: str
    context: str
