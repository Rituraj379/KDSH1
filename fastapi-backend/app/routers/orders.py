from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import current_user
from ..store import load_store, save_store

router = APIRouter(prefix="/api/orders", tags=["orders"])


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@router.get("/mine")
def my_orders(user_info: dict[str, Any] = Depends(current_user)) -> list[dict[str, Any]]:
    return [order for order in load_store()["orders"] if order["user"] == user_info["_id"]]


@router.post("")
def create_order(
    payload: dict[str, Any],
    user_info: dict[str, Any] = Depends(current_user),
) -> dict[str, Any]:
    if not payload.get("orderItems"):
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = {
        "_id": f"ord_{uuid4().hex}",
        "orderItems": payload["orderItems"],
        "shippingAddress": payload.get("shippingAddress", {}),
        "paymentMethod": payload.get("paymentMethod", "PayPal"),
        "itemsPrice": payload.get("itemsPrice", 0),
        "shippingPrice": payload.get("shippingPrice", 0),
        "taxPrice": payload.get("taxPrice", 0),
        "totalPrice": payload.get("totalPrice", 0),
        "user": user_info["_id"],
        "isPaid": False,
        "paidAt": None,
        "paymentResult": None,
        "isDelivered": False,
        "deliveredAt": None,
        "createdAt": _utc_now(),
    }

    store = load_store()
    store["orders"].append(order)
    save_store(store)
    return {"message": "New order created.", "order": order}


@router.get("/{order_id}")
def order_details(
    order_id: str,
    user_info: dict[str, Any] = Depends(current_user),
) -> dict[str, Any]:
    order = next((item for item in load_store()["orders"] if item["_id"] == order_id), None)
    if not order or order["user"] != user_info["_id"]:
        raise HTTPException(status_code=404, detail="Order not found.")
    return order


@router.put("/{order_id}/pay")
def pay_order(
    order_id: str,
    payment_result: dict[str, Any],
    user_info: dict[str, Any] = Depends(current_user),
) -> dict[str, Any]:
    store = load_store()
    order = next((item for item in store["orders"] if item["_id"] == order_id), None)
    if not order or order["user"] != user_info["_id"]:
        raise HTTPException(status_code=404, detail="Order not found.")

    order["isPaid"] = True
    order["paidAt"] = _utc_now()
    order["paymentResult"] = {
        "id": payment_result.get("id"),
        "status": payment_result.get("status"),
        "update_time": payment_result.get("update_time"),
        "email_address": payment_result.get("email_address"),
    }
    save_store(store)
    return {"message": "Order paid.", "order": order}
