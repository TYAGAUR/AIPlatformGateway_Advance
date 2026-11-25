from fastapi import APIRouter, HTTPException

from services.model_service import (
    get_all_models,
    get_model_by_id,
    process_ai_request
)

from schemas.request_schema import (
    AIRequest,
    AIResponse,
    PromptValidationRequest,
    PromptValidationResponse
)


router = APIRouter()


@router.get("/models")
def list_models():

    models = get_all_models()

    return {
        "count": len(models),
        "models": models
    }


@router.get("/models/{model_id}")
def retrieve_model(model_id: str):

    model = get_model_by_id(model_id)

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="AI model not found"
        )

    return model


@router.post(
    "/requests",
    response_model=AIResponse
)
def create_ai_request(request: AIRequest):

    response = process_ai_request(request)

    if response is None:
        raise HTTPException(
            status_code=404,
            detail="Requested AI model does not exist"
        )

    if response == "provider_mismatch":
        raise HTTPException(
            status_code=400,
            detail="Selected provider does not match the model"
        )

    return response


@router.post(
    "/requests/validate",
    response_model=PromptValidationResponse
)
def validate_prompt(request: PromptValidationRequest):

    cleaned_prompt = request.prompt.strip()

    return PromptValidationResponse(
        valid=True,
        prompt_length=len(cleaned_prompt),
        message="Prompt validation successful"
    )