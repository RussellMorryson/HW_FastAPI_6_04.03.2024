from fastapi import FastAPI, HTTPException, Depends  
from sqlalchemy.orm import Session

import logging
import uvicorn


import crud, models, schemas
from database import SessionLocal, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.User):
    query = user.insert().values(name=user.name, surname=user.surname, email=user.email, password = user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


# USER
# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.User, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/{user_email}", response_model=schemas.User)
def read_user_by_email(user_email: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user_email=user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# PRODUCT
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_user_by_email(db, title=product.title)
    if db_product:
        raise HTTPException(status_code=400, detail="Product is already registered")
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_product

@app.get("/products/{product_title}", response_model=schemas.Product)
def read_product_by_title(product_title: str, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_title=product_title)
    if db_product is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_product

# ORDER
@app.post("/order/", response_model=schemas.Order)
def create_order(order: schemas.Order,
                 db: Session = Depends(get_db)):    
    return crud.create_order(db=db, order=order)

if __name__ == '__main__':
    #unicorn.run(app)
    uvicorn.run(app, host="127.0.0.1", port=8000)