from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class BrandCreate(BaseModel):
    name: str


class ModelCreate(BaseModel):
    """
    Represents a model for creating an entity with a name and an optional average price.

    Attributes:
        name (str): The name of the entity.
        average_price (Optional[float]): The average price of the entity. Must be greater than or equal to 100,000.00 if provided.

    Methods:
        validate_price(cls, v):
            Validates the average_price field to ensure it is either None or a value greater than or equal to 100,000.00.
            Raises:
                ValueError: If the average_price is less than 100,000.00.
    """

    name: str
    average_price: Optional[float] = None

    @field_validator("average_price")
    def validate_price(cls, v):
        if v is not None and v < 0 or v > 0 and v < 100_000:
            raise ValueError(
                "El precio promedio debe siempre debe ser un valor mayor a 100,000.00"
            )
        return v


class ModelUpdate(BaseModel):
    """
    A Pydantic model representing an update to a model with validation for the average price.

    Attributes:
        average_price (float): The average price value that must be greater than or equal to 100,000.00.

    Methods:
        validate_price(cls, v):
            Validates that the average price is either 0 or greater than or equal to 100,000.00.
            Raises:
                ValueError: If the average price is less than 0 or between 0 and 100,000.00.
    """

    average_price: float

    @field_validator("average_price")
    def validate_price(cls, v):
        if v < 0 or v > 0 and v < 100_000:
            raise ValueError(
                "El precio promedio debe siempre debe ser un valor mayor a 100,000.00"
            )
        return v


class ModelResponse(BaseModel):
    """
    ModelResponse represents the structure of a response model with the following attributes:

    Attributes:
        id (int): The unique identifier for the model.
        name (str): The name of the model.
        average_price (Optional[float]): The average price associated with the model. This field is optional.
    """

    id: int
    name: str
    average_price: Optional[float]


class BrandResponse(BaseModel):
    """
    Represents the response model for a brand.

    Attributes:
        id (int): The unique identifier of the brand.
        name (str): The name of the brand.
        average_price (Optional[float]): The average price of the brand's products. Defaults to None.
    """

    id: int
    name: str
    average_price: Optional[float] = None
