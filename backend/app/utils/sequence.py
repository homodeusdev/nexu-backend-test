from app.config import database
from pymongo import ReturnDocument


async def get_next_sequence(name: str) -> int:
    """
    Asynchronously retrieves and increments the sequence number for a given name.

    This function interacts with a MongoDB collection to find and update a document
    with the specified name. If the document does not exist, it creates one with an
    initial sequence value. The sequence number is incremented atomically to ensure
    consistency in concurrent environments.

    Args:
        name (str): The name of the sequence to retrieve and increment.

    Returns:
        int: The updated sequence number after the increment.

    Raises:
        KeyError: If the "seq" field is not found in the retrieved document.

    Example:
        >>> # Assuming an existing MongoDB collection with a document {"_id": "order", "seq": 5}
        >>> next_seq = await get_next_sequence("order")
        >>> print(next_seq)
        6
    """
    counter = await database.counters.find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True,
    )
    return counter["seq"]
