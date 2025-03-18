from app.models import BrandCreate, BrandResponse, ModelCreate
from app.services import brand_service, model_service
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.get("/brands", response_model=list[BrandResponse])
async def list_brands():
    """
    Retrieve a list of all brands.

    Returns:
        list[BrandResponse]: A list of brand objects.
    """
    brands = await brand_service.get_all_brands()
    return brands


@router.post(
    "/brands", response_model=BrandResponse, status_code=status.HTTP_201_CREATED
)
async def add_brand(brand: BrandCreate):
    """
    Add a new brand.

    Args:
        brand (BrandCreate): The brand data to create.

    Returns:
        BrandResponse: The created brand object.

    Raises:
        HTTPException: If there is an error during brand creation.
    """
    new_brand, error = await brand_service.create_brand(brand)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_brand


@router.get("/brands/{brand_id}/models", response_model=list)
async def list_models_by_brand(brand_id: int):
    """
    Retrieve a list of models for a specific brand.

    Args:
        brand_id (int): The ID of the brand.

    Returns:
        list: A list of model objects.

    Raises:
        HTTPException: If the brand is not found.
    """
    brand = await brand_service.get_brand_by_id(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    models = await model_service.get_models_by_brand(brand_id)
    return models


@router.post("/brands/{brand_id}/models", status_code=status.HTTP_201_CREATED)
async def add_model_to_brand(brand_id: int, model: ModelCreate):
    """
    Add a new model to a specific brand.

    Args:
        brand_id (int): The ID of the brand.
        model (ModelCreate): The model data to create.

    Returns:
        dict: The created model object.

    Raises:
        HTTPException: If there is an error during model creation.
    """
    new_model, error = await model_service.create_model_for_brand(brand_id, model)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return new_model
