from util import DatabaseSession, RedisSession
from typing import Tuple
from bson.objectid import ObjectId
from dtypes import AddNewProductRequest
import json

class ProductService:
    __db_client: DatabaseSession
    __redis_client: RedisSession

    def __init__(self, dbc: DatabaseSession, rdc: RedisSession) -> None:
        self.__db_client = dbc
        self.__redis_client = rdc
    
    def add_new_product(self, product: AddNewProductRequest) -> Tuple[bool, str, dict | str | None]:
        success, product_id = self.__db_client.insert("products", product.model_dump())
        if not success:
            return False, "Failed to add product", None
        return True, "Product added successfully", {"product_id": product_id}
    
    def search_product(self, q: str, s_type: str) -> Tuple[bool, str, dict | list | None]:
        s_result = self.__redis_client.get(f"{s_type}:{q}")
        if s_result is not None:
            return True, "Product found", json.loads(s_result)
        if s_type not in ["name", "id", "category"]:
            return False, "Invalid search type", []
        success, products = self.__db_client.find("products", {s_type: q})
        if not success:
            return False, "No items found", []
        
        for product in products:
            product["_id"] = str(product["_id"])
        self.__redis_client.set(f"{s_type}:{q}", json.dumps(products), 300)
        return True, "Products found", products
    
    def get_product(self, product_id: str) -> Tuple[bool, str, dict | None]:
        product = self.__redis_client.get(f"product:{product_id}")
        if product is not None:
            return True, "Product found", json.loads(product)
        success, product = self.__db_client.findOne("products", {"_id": ObjectId(product_id)})
        if not success: 
            return False, "Product not found", None
        product["_id"] = str(product["_id"])
        self.__redis_client.set(f"product:{product_id}", json.dumps(product), 3600)
        return True, "Product found", product
    
    def get_product_listing(self) -> Tuple[bool, str, dict | None]:
        # Get a list of 20 random products from DB
        success, products = self.__db_client.find("products", {}, num_rec=20)
        if not success:
            return False, "No products found", None
        for product in products:
            product["_id"] = str(product["_id"])
        return True, "Products found", products