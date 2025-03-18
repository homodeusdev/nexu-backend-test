from app.config import brands_collection, models_collection
from app.models import ModelCreate, ModelUpdate
from app.utils.sequence import get_next_sequence


async def get_models_by_brand(brand_id: int):
    """
    Retrieve a list of models associated with a specific brand.

    This asynchronous function queries the `models_collection` database for models
    that match the given `brand_id`. It constructs a list of models, each containing
    the model's ID, name, and average price. If the average price is not available,
    it defaults to 0.

    Args:
        brand_id (int): The ID of the brand for which models are to be retrieved.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents
        a model with the following keys:
            - "id" (Any): The unique identifier of the model.
            - "name" (str): The name of the model.
            - "average_price" (float): The average price of the model, defaulting to 0
              if not available.
    """
    models = []
    async for model in models_collection.find({"brand_id": brand_id}):
        avg_price = model.get("average_price")
        if avg_price is None:
            avg_price = 0
        models.append(
            {"id": model["_id"], "name": model["name"], "average_price": avg_price}
        )
    return models


async def create_model_for_brand(brand_id: str, model: ModelCreate):
    """
    Creates a new model for a given brand.

    This function checks if the brand exists and if the model already exists for the brand.
    If the brand does not exist, it returns an error message. If the model already exists
    for the brand, it also returns an error message. Otherwise, it creates a new model
    with a unique ID and inserts it into the database.

    Args:
        brand_id (str): The ID of the brand to which the model belongs.
        model (ModelCreate): An object containing the details of the model to be created.

    Returns:
        tuple: A tuple containing:
            - dict: The newly created model as a dictionary, or None if an error occurred.
            - str: An error message if the operation failed, or None if it succeeded.
    """
    from app.services.brand_service import get_brand_by_id

    brand = await get_brand_by_id(brand_id)
    if not brand:
        return None, "La marca no existe"

    if await models_collection.find_one({"brand_id": brand_id, "name": model.name}):
        return None, "El modelo ya existe para la marca"

    next_id = await get_next_sequence("models")

    new_model = {
        "_id": next_id,
        "brand_id": brand_id,
        "name": model.name,
        "average_price": model.average_price,
    }
    result = await models_collection.insert_one(new_model)
    new_model["id"] = next_id
    return new_model, None


async def update_model(model_id: str, data: ModelUpdate):
    """
    Updates the average price of a model in the database.

    Args:
        model_id (str): The ID of the model to update, provided as a string.
        data (ModelUpdate): An instance of ModelUpdate containing the new average price.

    Returns:
        tuple: A tuple containing:
            - dict or None: The updated model as a dictionary if the update is successful, or None if the model does not exist.
            - str or None: An error message if the model does not exist, or None if the update is successful.

    Raises:
        ValueError: If the model_id cannot be converted to an integer.
    """
    numeric_model_id = int(model_id)
    model = await models_collection.find_one({"_id": numeric_model_id})
    if not model:
        return None, "El modelo no existe"
    await models_collection.update_one(
        {"_id": numeric_model_id}, {"$set": {"average_price": data.average_price}}
    )
    model["average_price"] = data.average_price
    model["id"] = numeric_model_id
    return model, None


async def get_models_filtered(greater: float = None, lower: float = None):
    """
    Retrieve a list of models filtered by their average price.

    This function queries a collection of models and filters them based on the
    specified `greater` and/or `lower` bounds for the `average_price` field.

    Args:
        greater (float, optional): The lower bound for the average price.
                                   Models with an average price greater than this value will be included.
        lower (float, optional): The upper bound for the average price.
                                 Models with an average price lower than this value will be included.

    Returns:
        list: A list of dictionaries, where each dictionary represents a model with the following keys:
            - "id" (str): The unique identifier of the model.
            - "name" (str): The name of the model.
            - "average_price" (float, optional): The average price of the model, if available.

    Raises:
        None: This function does not explicitly raise any exceptions.
    """
    query = {}
    if greater is not None and lower is not None:
        query["average_price"] = {"$gt": greater, "$lt": lower}
    elif greater is not None:
        query["average_price"] = {"$gt": greater}
    elif lower is not None:
        query["average_price"] = {"$lt": lower}

    models = []
    async for model in models_collection.find(query):
        models.append(
            {
                "id": model["_id"],
                "name": model["name"],
                "average_price": model.get("average_price"),
            }
        )
    return models
