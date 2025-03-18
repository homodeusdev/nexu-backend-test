import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import ModelCreate, ModelUpdate
from app.services.model_service import (create_model_for_brand,
                                        get_models_by_brand,
                                        get_models_filtered, update_model)


async def fake_find_models(query):
    if query.get("brand_id") == 1:
        for m in [
            {"_id": 10, "name": "Model1", "average_price": 100000},
            {"_id": 11, "name": "Model2", "average_price": 200000},
        ]:
            yield m
    else:
        if False:
            yield


@pytest.mark.asyncio
async def test_get_models_by_brand(monkeypatch):
    from app.config import models_collection

    monkeypatch.setattr(models_collection, "find", fake_find_models)

    models = await get_models_by_brand(1)
    assert len(models) == 2
    model1 = next(m for m in models if m["name"] == "Model1")
    model2 = next(m for m in models if m["name"] == "Model2")
    assert model1["average_price"] == 100000
    assert model2["average_price"] == 200000


async def fake_find(query):
    fake_models = [
        {"_id": 1, "name": "ModelA", "average_price": 150000},
        {"_id": 2, "name": "ModelB", "average_price": 250000},
        {"_id": 3, "name": "ModelC", "average_price": 0},
    ]
    for m in fake_models:
        yield m


@pytest.mark.asyncio
async def test_get_models_filtered(monkeypatch):
    from app.config import models_collection

    monkeypatch.setattr(models_collection, "find", fake_find)

    models = await get_models_filtered()
    assert len(models) == 3
    model_c = next(m for m in models if m["name"] == "ModelC")
    assert model_c["average_price"] == 0


@pytest.mark.asyncio
async def test_create_model_for_brand(monkeypatch):
    async def fake_get_brand_by_id(brand_id):
        if brand_id == 1:
            return {"_id": 1, "name": "Acura", "id": 1}
        return None

    async def fake_find_one(query):
        return None

    class FakeInsertResult:
        @property
        def inserted_id(self):
            return 1

    async def fake_insert_one(document):
        return FakeInsertResult()

    from app.config import models_collection

    monkeypatch.setattr(models_collection, "find_one", fake_find_one)
    monkeypatch.setattr(models_collection, "insert_one", fake_insert_one)

    from app.services import brand_service

    monkeypatch.setattr(brand_service, "get_brand_by_id", fake_get_brand_by_id)

    async def fake_get_next_sequence(name: str) -> int:
        return 1

    monkeypatch.setattr(
        "app.services.model_service.get_next_sequence", fake_get_next_sequence
    )

    from app.models import ModelCreate

    model, error = await create_model_for_brand(
        1, ModelCreate(name="ILX", average_price=300000)
    )
    assert error is None
    assert model["id"] == 1
    assert model["name"] == "ILX"
    assert model["average_price"] == 300000


@pytest.mark.asyncio
async def test_update_model(monkeypatch):
    fake_model = {"_id": 1, "name": "ILX", "average_price": 300000}

    async def fake_find_one(query):
        return fake_model

    async def fake_update_one(query, update):
        fake_model["average_price"] = update["$set"]["average_price"]

    from app.config import models_collection

    monkeypatch.setattr(models_collection, "find_one", fake_find_one)
    monkeypatch.setattr(models_collection, "update_one", fake_update_one)

    updated_model, error = await update_model("1", ModelUpdate(average_price=350000))
    assert error is None
    assert updated_model["average_price"] == 350000
