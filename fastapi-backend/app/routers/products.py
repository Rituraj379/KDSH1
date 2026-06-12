import copy

from fastapi import APIRouter, HTTPException

from ..data import DEFAULT_PRODUCTS
from ..store import load_store, save_store

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("")
def list_products() -> list[dict]:
    return load_store()["products"]


@router.get("/seed")
def seed_products() -> dict:
    store = load_store()
    store["products"] = copy.deepcopy(DEFAULT_PRODUCTS)
    save_store(store)
    return {"createdProducts": store["products"]}


@router.get("/{product_id}")
def product_details(product_id: str) -> dict:
    product = next(
        (item for item in load_store()["products"] if item["_id"] == product_id),
        None,
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product
