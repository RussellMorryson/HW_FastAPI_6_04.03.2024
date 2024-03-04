import uvicorn
import databases
import sqlalchemy

from fastapi import FastAPI
from pydantic import BaseModel, Field

from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = FastAPI()

#################################################################################################
# DB
DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("surname", sqlalchemy.String(64)),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password", sqlalchemy.String(512)),
    sqlalchemy.Column("date", sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column("status", sqlalchemy.String(64)))

products = sqlalchemy.Table(
        "products",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("title", sqlalchemy.String(64)),
        sqlalchemy.Column("description", sqlalchemy.String(64)),
        sqlalchemy.Column("price", sqlalchemy.Float),
        sqlalchemy.Column("quantity", sqlalchemy.Integer))

orders = sqlalchemy.Table(
        "orders",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("user_id", sqlalchemy.Integer, foreign_key = "users.id"),
        sqlalchemy.Column("product_id", sqlalchemy.Integer, foreign_key = "products.id"),
        sqlalchemy.Column("date", sqlalchemy.DateTime, default=datetime.utcnow),
        sqlalchemy.Column("status", sqlalchemy.String(64), default="In processing"))


engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)


#################################################################################################
# MODELS
class UserIn(BaseModel):
    name: str = Field(max_length=32, nullable=False)
    surname:str = Field(max_length=64, nullable=False)
    email: str = Field(max_length=128, nullable=False, unique=True)
    password: str = Field(nullable=False)

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

class User(BaseModel):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32, nullable=False)
    surname:str = Field(max_length=64, nullable=False)
    email: str = Field(max_length=128, nullable=False, unique=True)
    password: str = Field(nullable=False)
    date: datetime = Field(default=datetime.utcnow)
    status: str = Field(default="Active")
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class ProductIn(BaseModel):
    title: str = Field(max_length=64, nullable=False)
    description: str = Field(max_length=64, nullable=False)
    price: float = Field(gt = 0, default=0)
    quantity: int = Field(gt=0, default=0)

class Product(BaseModel):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=64, nullable=False)
    description: str = Field(max_length=64, nullable=False)
    price: float = Field(gt = 0, default=0)
    quantity: int = Field(gt=0, default=0)

class OrderIn(BaseModel):
    user_id: int = Field(foreign_key="User.id")
    product_id: int = Field(foreign_key = "Product.id")

class Order(BaseModel):
    __table_args__ = (sqlalchemy.UniqueConstraint("name", "user_id", name="user"))
    __table_args__ = (sqlalchemy.UniqueConstraint("title", "product_id", name="product"))
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key = "product.id")
    date: datetime = Field(default=datetime.utcnow)
    status: str = Field(max_length=64, default="In processing")

#################################################################################################
# CRUD COMMANDS

@app.get("/fake_users/{count}")
async def create_f_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}', 
                                      surname=f'user{i}',
                                      email=f'mail{i}@mail.ru',
                                      password = generate_password_hash('pass' + str(i)),
                                      #date = datetime.utcnow,
                                      status = "Active")

        await database.execute(query)
    return {'message': f'{count} fake users create'}


@app.get("/fake_products/{count}")
async def create_f_products(count: int):
    for i in range(count):
        query = products.insert().values(title=f'product{i}', 
                                         description=f'desc{i}',
                                         price=100.00+i,
                                         quantity=i)
        await database.execute(query)
    return {'message': f'{count} fake products create'}


@app.get("/fake_orders/{count}")
async def create_f_orders(count: int):
    for i in range(count):
        query = orders.insert().values(user_id=i,
                                       product_id = i,
                                       #date = datetime.utcnow,
                                       status = "In processing")
        await database.execute(query)
    return {'message': f'{count} fake orders create'}


# Точка входа
if __name__ == '__main__':    
    uvicorn.run(app, host="127.0.0.1", port=8000)