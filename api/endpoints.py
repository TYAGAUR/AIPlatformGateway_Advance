from fastapi import APIRouter, HTTPException

from services.model_service import (
    get_all_models,
    get_model_by_id,
    process_ai_request
)

from schemas.request_schema import AIRequest, AIResponse


router = APIRouter()


# GET: List all available AI models
@router.get("/models")
def list_models():

    models = get_all_models()

    return {
        "count": len(models),
        "models": models
    }


# GET: Retrieve one specific model
@router.get("/models/{model_id}")
def retrieve_model(model_id: str):

    model = get_model_by_id(model_id)

    if model is None:
        raise HTTPException(
            status_code=404,
            detail="AI model not found"
        )

    return model


# POST: Submit an AI request
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

    return response