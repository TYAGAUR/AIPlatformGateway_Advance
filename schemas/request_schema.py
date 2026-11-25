from pydantic import BaseModel, Field, field_validator
from typing import Literal


class AIRequest(BaseModel):

    model: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="AI model identifier"
    )

    prompt: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="Prompt submitted by the user"
    )

    max_tokens: int = Field(
        default=500,
        ge=1,
        le=4000
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0
    )

    provider: Literal[
        "OpenAI",
        "Anthropic",
        "Google"
    ] | None = None

    stream: bool = False

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Prompt cannot contain only spaces"
            )

        return cleaned_value

    @field_validator("model")
    @classmethod
    def validate_model(cls, value):

        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError(
                "Model name cannot be empty"
            )

        return cleaned_value


class AIResponse(BaseModel):

    request_id: str

    model: str

    status: str

    input_tokens: int

    output_tokens: int

    total_tokens: int

    message: str

    provider: str | None = None


class PromptValidationRequest(BaseModel):

    prompt: str = Field(
        ...,
        min_length=5,
        max_length=10000
    )


class PromptValidationResponse(BaseModel):

    valid: bool

    prompt_length: int

    message: str


class GenerationConfig(BaseModel):

    max_tokens: int = Field(
        default=500,
        ge=1,
        le=4000
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0
    )


class AdvancedAIRequest(BaseModel):

    model: str

    prompt: str

    generation: GenerationConfig

    metadata: dict[str, str] = Field(
        default_factory=dict
    )