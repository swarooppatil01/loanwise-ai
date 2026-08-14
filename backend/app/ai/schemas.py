from pydantic import BaseModel, Field


class AIChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000,
    )
    application_id: int | None = None


class AIChatResponse(BaseModel):
    answer: str
    application_id: int | None = None
