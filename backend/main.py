from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Maze
from database import SessionLocal, Base, engine
from utils import check_moves 
from typing import List
from schemas import MazeResponse, VerifyResponse


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Maze API",
    description="An API to fetch mazes and validate moves in a maze-solving game.",)

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "Maze API running"}

@app.get("/mazes", response_model=List[MazeResponse])
def get_mazes():
    db = SessionLocal()
    try:
        return db.query(Maze).all()
    finally:
        db.close()

@app.get("/mazes/{maze_id}", response_model=MazeResponse)
def get_maze(maze_id: int):
    db = SessionLocal()
    try:
        maze = db.query(Maze).filter(Maze.id == maze_id).first()
        if not maze:
            raise HTTPException(status_code=404, detail="Maze not found")
        return maze
    finally:
        db.close()

@app.post("/mazes/{maze_id}/verify", response_model=VerifyResponse)
async def verify_maze(maze_id: int, request: Request):
    db = SessionLocal()
    try:
        maze = db.query(Maze).filter(Maze.id == maze_id).first()
        if not maze:
            raise HTTPException(status_code=404, detail="Maze not found")

        data = await request.json()
        moves = data.get("moves", [])

        result = check_moves(maze.grid, moves)

        return {"message": result}
    finally:
        db.close()