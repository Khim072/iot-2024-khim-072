from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

# books
@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], detail=book['detail'], synopsis=book['synopsis'], category=book['category'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.patch('/books/{book_id}')
async def update_book(book_id: int, book: dict, db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        return {
        'message': 'Book not found'
    }
    if 'title' in book:
        existing_book.title = book['title']
    if 'author' in book:
        existing_book.author = book['author']
    if 'year' in book:
        existing_book.year = book['year']
    if 'is_published' in book:
        existing_book.is_published = book['is_published']
    if 'detail' in book:
        existing_book.detail = book['detail']
    if 'synopsis' in book:
        existing_book.synopsis = book['synopsis']
    if 'category' in book:
        existing_book.category = book['category']
    db.commit()
    db.refresh(existing_book)
    return existing_book

@router_v1.delete('/books/{book_id}')
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    existing_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not existing_book:
        return {
        'message': 'Book not found'
    }
    db.delete(existing_book)
    db.commit()
    return {"detail": "Book deleted successfully"}

#coffee
@router_v1.get('/coffees')
async def get_coffee(db: Session = Depends(get_db)):
    return db.query(models.Coffee).all()

@router_v1.get('/coffees/{coffee_id}')
async def get_coffee(coffee_id: int, db: Session = Depends(get_db)):
    return db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()

@router_v1.post('/coffees')
async def create_coffee(coffee: dict, response: Response, db: Session = Depends(get_db)):
    new_coffee = models.Coffee(name=coffee['name'], description=coffee['description'], price=coffee['price'])
    db.add(new_coffee)
    db.commit()
    db.refresh(new_coffee)
    response.status_code = 201
    return new_coffee

@router_v1.patch('/coffees/{coffee_id}')
async def update_coffee(coffee_id: int, coffee: dict, db: Session = Depends(get_db)):
    existing_coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not existing_coffee:
        return {
        'message': 'coffee not found'
    }
    if 'name' in coffee:
        existing_coffee.name = coffee['name']
    if 'description' in coffee:
        existing_coffee.description = coffee['description']
    if 'price' in coffee:
        existing_coffee.price = coffee['price']
    db.commit()
    db.refresh(existing_coffee)
    return existing_coffee

@router_v1.delete('/coffees/{coffee_id}')
async def delete_coffee(coffee_id: int, db: Session = Depends(get_db)):
    existing_coffee = db.query(models.Coffee).filter(models.Coffee.id == coffee_id).first()
    if not existing_coffee:
        return {
        'message': 'coffee not found'
    }
    db.delete(existing_coffee)
    db.commit()
    return {"detail": "coffee deleted successfully"}

#orders
@router_v1.get('/orders')
async def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()

@router_v1.get('/orders/{order_id}')
async def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

@router_v1.post('/orders')
async def create_order(order: dict, response: Response, db: Session = Depends(get_db)):
    new_order = models.Order(coffee_id=order['coffee_id'], quantity=order['quantity'], total_price=order['total_price'], notes=order['notes'])
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    response.status_code = 201
    return new_order

@router_v1.patch('/orders/{order_id}')
async def update_order(response: Response ,order_id: int, order: dict, db: Session = Depends(get_db),):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for key, value in order.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
        return db_order
    else:
        return response.status_code == 404

@router_v1.delete('/orders/{order_id}')
async def delete_order(response: Response, order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
        return {"message": "Order deleted successfully"}
    else:
        return response.status_code == 404

# Assignment 1

@router_v1.get('/infos')
async def get_infos(db: Session = Depends(get_db)):
    return db.query(models.Info).all()

@router_v1.get('/infos/{info_id}')
async def get_info(info_id: int, db: Session = Depends(get_db)):
    return db.query(models.Info).filter(models.Info.id == info_id).first()

@router_v1.post('/infos')
async def add_info(info: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newinfo = models.Info(id=info['id'], fname=info['fname'], lname=info['lname'], nickname=info['nickname'], num_id=info['num_id'], dob=info['dob'], gender=info['gender'])
    db.add(newinfo)
    db.commit()
    db.refresh(newinfo)
    response.status_code = 201
    return newinfo

@router_v1.patch('/infos/{info_id}')
async def update_info(info_id: int, info: dict, response: Response, db: Session = Depends(get_db)):
    info = db.query(models.Info).filter(models.Info.id == info_id).first()
    if (info is None):
        response.status_code = 400
        return {
            "message" : "Information not found."
        }
    keys = ["id", "fname", "lname", "nickname", "num_id", "dob", "gender"]
    for key in keys:
        if key in info:
            setattr(info, key, info[key])
    db.commit()
    response.status_code = 201
    return {
        "message" : "Information edited successfully"
    }

@router_v1.delete('/infos/{info_id}')
async def delete_info(info_id: int, response: Response, db: Session = Depends(get_db)):
    stu = db.query(models.Info).filter(models.Info.id == info_id).first()
    if (info is not None):
        db.delete(info)
        db.commit()
        response.status_code = 201
        return {
            "message" : "delete info successfully"
        }
    response.status_code = 400
    return {
        "message" : "Information not found."
    }

app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
