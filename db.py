from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from contextlib import contextmanager

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    model = Column(String(50), nullable=False)  # PS5, Xbox Series X
    params = Column(String(200))  # "4K, 120Hz, 1TB SSD"
    available_count = Column(Integer, default=0)
    price_per_day = Column(Float, default=0.0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    delivery_address = Column(String(200))
    items = Column(String(500))  # JSON строкой: '[{"id":1,"count":2}]'
    total_price = Column(Float)
    status = Column(String(20), default='new')  # new, confirmed, delivered
    created_at = Column(DateTime, default=datetime.utcnow)

# Инициализация БД
engine = create_engine('sqlite:///rent.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
