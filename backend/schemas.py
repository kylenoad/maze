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
