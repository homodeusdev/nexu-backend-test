import json
from pathlib import Path

from app.config import brands_collection, models_collection
from app.models import BrandCreate, ModelCreate
from app.routes import brands, models
from app.services.brand_service import create_brand, get_brand_by_id
from app.services.model_service import create_model_for_brand
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Backend de Agencia de Automóviles")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brands.router)
app.include_router(models.router)


async def get_or_create_brand_by_name(brand_name: str):
    brand = await brands_collection.find_one({"name": brand_name})
    if brand:
        brand["id"] = brand["_id"]
        return brand
    new_brand, error = await create_brand(BrandCreate(name=brand_name))
    if error:
        return None
    return new_brand


@app.on_event("startup")
async def startup_db_population():
    """
    Populates the database with initial data from a JSON file if the database is empty.

    This function checks if the `brands_collection` in the database already contains documents.
    If it does, the function skips the population process. Otherwise, it reads data from a
    `models.json` file located in the parent directory, processes the data, and inserts it
    into the database.

    The function performs the following steps:
    1. Checks if the database already contains brand documents.
    2. Reads the `models.json` file if it exists.
    3. Iterates through the data in the JSON file and:
       - Retrieves or creates a brand by its name.
       - Checks if a model for the brand already exists in the database.
       - Creates a new model for the brand if it does not exist.
    4. Logs messages for each step, including errors and successful insertions.

    Notes:
    - If the `models.json` file is not found, the function logs a message and exits.
    - If the `average_price` of a model is less than or equal to 0, it is set to 0.

    Raises:
        Any exceptions raised by the database operations or file handling will propagate.

    Dependencies:
        - `brands_collection`: MongoDB collection for brand documents.
        - `models_collection`: MongoDB collection for model documents.
        - `get_or_create_brand_by_name`: Async function to retrieve or create a brand.
        - `create_model_for_brand`: Async function to create a model for a brand.
        - `ModelCreate`: Data model for creating a new model.

    """
    if await brands_collection.count_documents({}) > 0:
        print("La base de datos ya fue poblada. Saltando carga inicial.")
        return

    file_path = Path("../models.json")
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as f:
            models_data = json.load(f)
        for item in models_data:
            brand_name = item.get("brand_name")
            model_name = item.get("name")
            average_price = item.get("average_price")

            if average_price is not None and average_price <= 0:
                average_price = 0

            brand = await get_or_create_brand_by_name(brand_name)
            if not brand:
                print(f"Error al procesar la marca: {brand_name}")
                continue

            existing_model = await models_collection.find_one(
                {"brand_id": brand["id"], "name": model_name}
            )
            if existing_model:
                print(
                    f"El modelo {model_name} para la marca {brand_name} ya existe. Saltando."
                )
                continue

            new_model, error = await create_model_for_brand(
                brand["id"], ModelCreate(name=model_name, average_price=average_price)
            )
            if error:
                print(
                    f"Error al crear el modelo {model_name} para la marca {brand_name}: {error}"
                )
            else:
                print(
                    f"Modelo {model_name} insertado exitosamente para la marca {brand_name}"
                )
    else:
        print("No se encontró el archivo models.json para la población inicial.")
