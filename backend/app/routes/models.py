from app.models import ModelUpdate
from app.services import model_service
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.put("/models/{model_id}")
async def update_model(model_id: int, data: ModelUpdate):
    """
    Update an existing model with the provided data.

    Args:
        model_id (int): The ID of the model to be updated.
        data (ModelUpdate): The data to update the model with.

    Returns:
        The updated model object.

    Raises:
        HTTPException: If an error occurs during the update process,
                       an HTTP 400 exception is raised with the error details.
    """
    updated_model, error = await model_service.update_model(model_id, data)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return updated_model


@router.get("/models", response_model=list)
async def list_models(greater: float = None, lower: float = None):
    """
    Retrieve a list of models filtered by optional greater and lower bounds.

    Args:
        greater (float, optional): The lower bound for filtering models. Defaults to None.
        lower (float, optional): The upper bound for filtering models. Defaults to None.

    Returns:
        list: A list of models that meet the filtering criteria.
    """
    models = await model_service.get_models_filtered(greater, lower)
    return models
