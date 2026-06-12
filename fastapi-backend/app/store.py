import copy
import json
import os
from pathlib import Path
from typing import Any

from .data import DEFAULT_PRODUCTS
from .security import hash_password

BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_STORE_PATH = BASE_DIR / "data" / "store.json"


def _store_path() -> Path:
    configured_path = os.getenv("STORE_PATH")
    if not configured_path:
        return DEFAULT_STORE_PATH

    path = Path(configured_path)
    return path if path.is_absolute() else BASE_DIR / path


def _seed_users() -> list[dict[str, Any]]:
    return [
        {
            "_id": "usr_admin",
            "name": "Admin User",
            "email": "admin2023@gmail.com",
            "password": hash_password("1234"),
            "isAdmin": True,
        },
        {
            "_id": "usr_demo",
            "name": "Demo User",
            "email": "demo@example.com",
            "password": hash_password("1234"),
            "isAdmin": False,
        },
    ]


def fresh_store() -> dict[str, Any]:
    return {
        "products": copy.deepcopy(DEFAULT_PRODUCTS),
        "users": _seed_users(),
        "orders": [],
    }


def load_store() -> dict[str, Any]:
    path = _store_path()
    if not path.exists():
        store = fresh_store()
        save_store(store)
        return store

    with path.open("r", encoding="utf-8") as file:
        store = json.load(file)

    store.setdefault("products", copy.deepcopy(DEFAULT_PRODUCTS))
    store.setdefault("users", _seed_users())
    store.setdefault("orders", [])
    return store


def save_store(store: dict[str, Any]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(store, file, indent=2)


def public_user(user: dict[str, Any]) -> dict[str, Any]:
    return {
        "_id": user["_id"],
        "name": user["name"],
        "email": user["email"],
        "isAdmin": user.get("isAdmin", False),
    }
