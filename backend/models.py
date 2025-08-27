from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from database import Base 

class Maze(Base):
    __tablename__ = "mazes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    grid = Column(JSONB, nullable=False)
