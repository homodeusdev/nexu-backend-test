from app.config import brands_collection, models_collection
from app.models import BrandCreate
from app.utils.sequence import get_next_sequence


async def get_all_brands():
    """
    Retrieve all brands from the database along with their average model prices.

    This function fetches all brand documents from the `brands_collection` and calculates
    the average price of their associated models from the `models_collection`. The result
    is a list of dictionaries containing the brand's ID, name, and average price.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
            - id (int): The brand's ID, converted to an integer. If conversion fails, defaults to 0.
            - name (str): The name of the brand.
            - average_price (float): The average price of the brand's models, rounded to 2 decimal places.
              If no models have prices, defaults to 0.
    """
    brands = []
    async for brand in brands_collection.find():
        models_cursor = models_collection.find({"brand_id": brand["_id"]})
        prices = [
            m.get("average_price")
            async for m in models_cursor
            if m.get("average_price") is not None
        ]
        average_price = round(sum(prices) / len(prices), 2) if prices else 0

        id_value = brand["_id"]
        if not isinstance(id_value, int):
            try:
                id_value = int(str(id_value), 16)
            except Exception:
                id_value = 0

        brands.append(
            {"id": id_value, "name": brand["name"], "average_price": average_price}
        )
    return brands


async def create_brand(brand: BrandCreate):
    """
    Creates a new brand in the database.

    Args:
        brand (BrandCreate): An object containing the details of the brand to be created.

    Returns:
        tuple: A tuple containing:
            - dict: The newly created brand with its ID, or None if the brand already exists.
            - str: An error message if the brand already exists, otherwise None.

    Notes:
        - If a brand with the same name already exists in the database, the function will return None and an error message.
        - The function generates a new unique ID for the brand using the `get_next_sequence` function.
    """
    if await brands_collection.find_one({"name": brand.name}):
        return None, "La marca ya existe"

    next_id = await get_next_sequence("brands")
    new_brand = {"_id": next_id, "name": brand.name}
    result = await brands_collection.insert_one(new_brand)
    new_brand["id"] = next_id
    return new_brand, None


async def get_brand_by_id(brand_id: str):
    """
    Retrieve a brand document from the database by its ID.

    Args:
        brand_id (str): The ID of the brand as a string. It will be converted to an integer.

    Returns:
        dict or None: The brand document if found, or None if the ID is invalid or the brand does not exist.
    """
    try:
        numeric_brand_id = int(brand_id)
    except ValueError:
        return None
    brand = await brands_collection.find_one({"_id": numeric_brand_id})
    return brand
