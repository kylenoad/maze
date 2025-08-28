from pydantic import BaseModel
from typing import List, Literal

class MazeBase(BaseModel):
    name: str
    grid: List[List[str]]  

class MazeResponse(MazeBase):
    id: int

    class Config:
        orm_mode = True  

class MovesRequest(BaseModel):
    moves: List[Literal["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]]

class VerifyResponse(BaseModel):
    message: str


class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str