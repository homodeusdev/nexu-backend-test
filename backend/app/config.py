import os

"""
This module is responsible for configuring the database connection and collections
used in the application.

Modules:
    os: Provides a way of using operating system dependent functionality.
    motor.motor_asyncio: Provides an asynchronous MongoDB driver.
    dotenv: Loads environment variables from a .env file.

Environment Variables:
    MONGO_DETAILS: The MongoDB connection string. Defaults to "mongodb://localhost:27017" 
                   if not provided.

Attributes:
    MONGO_DETAILS (str): The MongoDB connection string.
    client (AsyncIOMotorClient): The asynchronous MongoDB client instance.
    database (AsyncIOMotorDatabase): The MongoDB database instance.
    brands_collection (AsyncIOMotorCollection): The MongoDB collection for "brands".
    models_collection (AsyncIOMotorCollection): The MongoDB collection for "models".
"""

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()


MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client["pinguea-test"]

brands_collection = database.get_collection("brands")
models_collection = database.get_collection("models")
