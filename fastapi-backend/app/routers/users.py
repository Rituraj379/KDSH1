from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..dependencies import current_user
from ..security import create_access_token, hash_password, verify_password
from ..store import load_store, public_user, save_store

router = APIRouter(prefix="/api/users", tags=["users"])


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class SignInRequest(BaseModel):
    email: str
    password: str


class ProfileUpdateRequest(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


def _with_token(user: dict[str, Any]) -> dict[str, Any]:
    response = public_user(user)
    response["token"] = create_access_token(user)
    return response


@router.get("/seed")
def seed_users() -> dict:
    store = load_store()
    created_users = [public_user(user) for user in store["users"]]
    return {"createdUsers": created_users}


@router.post("/signin")
def signin(payload: SignInRequest) -> dict[str, Any]:
    store = load_store()
    user = next((item for item in store["users"] if item["email"] == payload.email), None)
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return _with_token(user)


@router.post("/register")
def register(payload: RegisterRequest) -> dict[str, Any]:
    store = load_store()
    existing_user = next(
        (item for item in store["users"] if item["email"].lower() == payload.email.lower()),
        None,
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    user = {
        "_id": f"usr_{uuid4().hex}",
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
        "isAdmin": False,
    }
    store["users"].append(user)
    save_store(store)
    return _with_token(user)


@router.get("/{user_id}")
def user_details(user_id: str, _: dict[str, Any] = Depends(current_user)) -> dict[str, Any]:
    user = next((item for item in load_store()["users"] if item["_id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return public_user(user)


@router.put("/profile")
def update_profile(
    payload: ProfileUpdateRequest,
    user_info: dict[str, Any] = Depends(current_user),
) -> dict[str, Any]:
    store = load_store()
    user = next((item for item in store["users"] if item["_id"] == user_info["_id"]), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.email:
        duplicate = next(
            (
                item
                for item in store["users"]
                if item["email"].lower() == payload.email.lower() and item["_id"] != user["_id"]
            ),
            None,
        )
        if duplicate:
            raise HTTPException(status_code=400, detail="Email already registered.")
        user["email"] = payload.email

    if payload.name:
        user["name"] = payload.name
    if payload.password:
        user["password"] = hash_password(payload.password)

    save_store(store)
    return _with_token(user)
