from fastapi import APIRouter, Response, Query
from typing import Annotated
from dtypes import AddNewProductRequest, make_response
from util import DatabaseSession, RedisSession
from service import ProductService

router = APIRouter(prefix="/api/v1/products", tags=["product"])
product_service = ProductService(
    dbc=DatabaseSession(), 
    rdc=RedisSession()
)

@router.post("/")
def add_new_product(request: AddNewProductRequest, response: Response):
    success, msg, data = product_service.add_new_product(request)
    if not success:
        return make_response(response, 500, msg)
    return make_response(response, 200, msg, data)

@router.get("/search")
def search_product(response: Response, q: Annotated[str, Query()] = "", s_type: Annotated[str, Query()] = "id"):
    if s_type not in ["name", "id", "category"]:
        return make_response(response, 400, "Invalid search type")
    _, msg, data = product_service.search_product(q, s_type)
    return make_response(response, 200, msg, data)

@router.get("/listing")
def get_product_listing(response: Response):
    _, msg, data = product_service.get_product_listing()
    return make_response(response, 200, msg, data)

@router.get("/{product_id}")
def get_product(product_id: str, response: Response):
    success, msg, data = product_service.get_product(product_id)
    if not success:
        return make_response(response, 404, msg)
    return make_response(response, 200, "Product found", data)

@router.put("/{product_id}")
def update_product(product_id: str, request: AddNewProductRequest, response: Response):
    print(product_id, request)
    return make_response(response, 200, "Product updated successfully")

@router.delete("/{product_id}")
def delete_product(product_id: str, response: Response):
    print(product_id)
    return make_response(response, 200, "Product deleted successfully")