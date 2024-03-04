from pydantic import BaseModel

# PRODUCT
class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    quantity: int

    class Config:
        orm_mode = True

# ORDER
class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: str
    status: str

    user: int
    product: int

    class Config:
        orm_mode = True

# USER
class User(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    password: str
    status: str

    order: int

    class Config:
        orm_mode = True