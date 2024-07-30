from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)
    detail = Column(String, index=True)
    synopsis = Column(String, index=True)
    category = Column(String, index=True)

class Coffee(Base):
    __tablename__ = 'coffees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    coffee_id = Column(Integer, ForeignKey('coffees.id'))
    quantity = Column(Integer, index=True)
    total_price = Column(Integer, index=True)
    notes = Column(String, index=True)

class Info(Base):
    __tablename__ = 'infos'

    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String, index=True)
    lname = Column(String, index=True)
    nickname = Column(String, index=True)
    num_id = Column(String, index=True)
    dob = Column(String, index=True)
    gender = Column(String, index=True)
