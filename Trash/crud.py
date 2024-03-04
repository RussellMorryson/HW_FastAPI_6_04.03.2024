from sqlalchemy.orm import Session
import models, schemas

# USER
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        name = user.name,
        surname = user.surname,
        email=user.email, 
        password = user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# PRODUCT
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_title(db: Session, title: int):
    return db.query(models.Product).filter(models.Product.title == title).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(
        title = product.title,
        description = product.description,
        price = product.price,
        quantity = product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ORDER
def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: schemas.Order):
    db_order = models.Product(
        user_id = order.user, 
        product = order.product,
        status = order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order