import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import BrandCreate
from app.services.brand_service import (create_brand, get_all_brands,
                                        get_brand_by_id)


class FakeCursor:
    def __init__(self, data):
        self.data = data

    async def __aiter__(self):
        for d in self.data:
            yield d


async def fake_find_models(query):
    if query.get("brand_id") == 1:
        async for m in FakeCursor(
            [{"average_price": 100000}, {"average_price": 200000}]
        ):
            yield m
    else:
        async for m in FakeCursor([]):
            yield m


@pytest.mark.asyncio
async def test_get_all_brands(monkeypatch):
    fake_brands = [{"_id": 1, "name": "Acura"}]

    async def fake_find_brand(query=None):
        for b in fake_brands:
            yield b

    from app.config import brands_collection, models_collection

    monkeypatch.setattr(brands_collection, "find", fake_find_brand)
    monkeypatch.setattr(models_collection, "find", fake_find_models)

    brands = await get_all_brands()
    assert len(brands) == 1
    assert brands[0]["average_price"] == 150000.00


@pytest.mark.asyncio
async def test_create_brand(monkeypatch):
    async def fake_find_one(query):
        return None

    class FakeInsertResult:
        @property
        def inserted_id(self):
            return 1

    async def fake_insert_one(document):
        return FakeInsertResult()

    from app.config import brands_collection

    monkeypatch.setattr(brands_collection, "find_one", fake_find_one)
    monkeypatch.setattr(brands_collection, "insert_one", fake_insert_one)

    from app.services import brand_service

    async def fake_get_next_sequence(name: str) -> int:
        return 1

    monkeypatch.setattr(brand_service, "get_next_sequence", fake_get_next_sequence)

    brand, error = await create_brand(BrandCreate(name="Acura"))
    assert error is None
    assert brand["id"] == 1
    assert brand["name"] == "Acura"


@pytest.mark.asyncio
async def test_get_brand_by_id(monkeypatch):
    fake_brand = {"_id": 1, "name": "Acura", "id": 1}

    async def fake_find_one(query):
        if query.get("_id") == 1:
            return fake_brand
        return None

    from app.config import brands_collection

    monkeypatch.setattr(brands_collection, "find_one", fake_find_one)

    brand = await get_brand_by_id("1")
    assert brand is not None
    assert brand["id"] == 1
    assert brand["name"] == "Acura"
