from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Maze, User
from database import SessionLocal, Base, engine
from utils import check_moves 
from typing import List
from schemas import MazeResponse, VerifyResponse, UserCreate, UserResponse, Token
from auth import hash_password, verify_password, create_access_token
from fastapi import Depends
from auth import get_current_user
from models import User


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
def get_mazes(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        return db.query(Maze).all()
    finally:
        db.close()

@app.get("/mazes/{maze_id}", response_model=MazeResponse)
def get_maze(maze_id: int, current_user: User = Depends(get_current_user)):
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

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    db = SessionLocal()
    try:
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = User(
            username=user.username,
            hashed_password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()

@app.post("/login", response_model=Token)
def login(user: UserCreate):
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token({"sub": db_user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()