import uuid

from config.models_config import AVAILABLE_MODELS

from schemas.request_schema import (
    AIRequest,
    AIResponse
)


def get_all_models():

    return list(AVAILABLE_MODELS.values())


def get_model_by_id(model_id: str):

    return AVAILABLE_MODELS.get(model_id)


def process_ai_request(request: AIRequest):

    model = get_model_by_id(request.model)

    if model is None:
        return None

    # Validate provider if the caller supplied one
    if (
        request.provider is not None
        and request.provider != model["provider"]
    ):
        return "provider_mismatch"

    request_id = f"req_{uuid.uuid4().hex[:8]}"

    # Illustrative token estimation only
    input_tokens = len(request.prompt.split())

    output_tokens = min(
        request.max_tokens,
        max(1, int(input_tokens * 1.5))
    )

    total_tokens = input_tokens + output_tokens

    response = AIResponse(
        request_id=request_id,
        model=request.model,
        status="success",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        message="Request validated and simulated successfully",
        provider=model["provider"]
    )

    return response