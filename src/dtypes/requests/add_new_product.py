from pydantic import BaseModel

class AddNewProductRequest(BaseModel):
    name: str
    price: float
    description: str
    category: str
    images: list[str]