from pydantic import BaseModel, Field


class UserInput(BaseModel):
    message: str = Field(..., max_length=1000, description="Texto del usuario (máx. 1000 caracteres)")