from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    model: str = Field(
        ...,
        description="AI model identifier"
    )

    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt submitted by the user"
    )

    max_tokens: int = Field(
        default=500,
        ge=1,
        le=4000,
        description="Maximum output tokens"
    )


class AIResponse(BaseModel):
    request_id: str
    model: str
    status: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    message: str