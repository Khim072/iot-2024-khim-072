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

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

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
