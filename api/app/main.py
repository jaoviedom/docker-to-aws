import time
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from .database import engine, Base, get_db
from .models import Product

app = FastAPI(title="Backend API")


@app.on_event("startup")
def startup_db_client():
    retries = 5
    while retries > 0:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            retries -= 1
            time.sleep(3)


@app.get("/api/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.post("/api/products")
def create_product(name: str, price: str, db: Session = Depends(get_db)):
    product = Product(name=name, price=price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
