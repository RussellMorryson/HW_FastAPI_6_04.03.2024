from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# USER
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Active")

    order = relationship("Order", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,  password):
	    return check_password_hash(self.password, password)
    
# PRODUCT
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Float, default=0.00)
    quantity = Column(Integer, default=0)

    order = relationship("Order", back_populates="product")

# ORDER
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False, default="In processing")

    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")