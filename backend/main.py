from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Maze
from database import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"msg": "Maze API running"}

@app.get("/mazes")
def get_mazes(db: Session = Depends(get_db)):
    return db.query(Maze).all()

@app.get("/mazes/{maze_id}")
def get_maze(maze_id: int, db: Session = Depends(get_db)):
    maze = db.query(Maze).filter(Maze.id == maze_id).first()
    if not maze:
        raise HTTPException(status_code=404, detail="Maze not found")
    return maze
