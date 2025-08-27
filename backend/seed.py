from models import Maze
from database import Base, engine, SessionLocal

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    maze1 = Maze(
        name="Maze 1",
        grid=[
            ["S", "W", "P2", "W", "W", "", "", "P1"],
            ["", "W", "K", "W", "", "", "", "W"],
            ["", "W", "W", "W", "", "W", "", "W"],
            ["", "W", "", "", "", "W", "", "W"],
            ["", "W", "", "W", "W", "W", "", "W"],
            ["", "", "", "W", "", "", "", "W"],
            ["", "W", "", "W", "", "W", "W", "W"],
            ["", "W", "", "W", "", "", "D", "G"],
        ]
    )

    maze2 = Maze(
        name="Maze 2",
        grid=[
            ["S", "W", "W", "W", "W", "W", "W", "W"],
            ["", "W", "", "", "", "", "", ""],
            ["", "W", "", "W", "W", "W", "W", ""],
            ["", "W", "", "", "P1", "W", "", ""],
            ["", "W", "D", "W", "W", "", "", "W"],
            ["", "W", "G", "W", "", "", "W", "P2"],
            ["", "W", "W", "W", "", "W", "W", "K"],
            ["", "", "", "", "", "", "", "W"],
        ]
    )

    db.add_all([maze1, maze2])
    db.commit()
    db.close()
    print("Seeded mazes successfully.")

if __name__ == "__main__":
    seed()
