import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = FastAPI()

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                      sqlalchemy.Column("name", sqlalchemy.String(32)),
                      sqlalchemy.Column("email", sqlalchemy.String(128)),

                      )

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

class UserIn(BaseModel):
    name: str = Field(max_length=32, nullable=False)
    surname:str = Field(max_length=64, nullable=False)
    email: str = Field(max_length=128, nullable=False, unique=True)
    password: str = Field(max_length=128, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

class User(BaseModel):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32, nullable=False)
    surname:str = Field(max_length=64, nullable=False)
    email: str = Field(max_length=128, nullable=False, unique=True)
    password: str = Field(max_length=128, nullable=False)
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
    status: str = Field(max_length=64, default="In processing")



@app.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i}', email=f'mail{i}@mail.ru')
        await database.execute(query)
    return {'message': f'{count} fake users create'}
    





# Точка входа
if __name__ == '__main__':    
    uvicorn.run(app, host="127.0.0.1", port=8000)