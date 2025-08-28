import React, { useState, useEffect } from "react";
import Tile from "./Tile";

const findPortal = (maze, portal) => {
  for (let row = 0; row < maze.length; row++) {
    for (let col = 0; col < maze[row].length; col++) {
      if (maze[row][col] === portal) return [row, col];
    }
  }
  return null;
};

const MazeGame = ({ mazeId }) => {
  const [maze, setMaze] = useState([]);
  const [position, setPosition] = useState([0, 0]);
  const [message, setMessage] = useState("");
  const [hasKey, setHasKey] = useState(false);
  const [moves, setMoves] = useState([]);

  useEffect(() => {
    const fetchMaze = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch(`http://localhost:8000/mazes/${mazeId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) throw new Error("Failed to fetch maze");
        const data = await response.json();
        setMaze(data.grid);
        setPosition([0, 0]);
        setHasKey(false);
        setMessage("");
        setMoves([]);
      } catch (err) {
        console.error(err);
        setMessage("Error loading maze");
      }
    };

    fetchMaze();
  }, [mazeId]);

  useEffect(() => {
    if (!maze.length) return;

    const handleKeyDown = (e) => {
      let row = position[0];
      let col = position[1];

      let newRow = row;
      let newCol = col;

      if (e.key === "ArrowUp") newRow--;
      if (e.key === "ArrowDown") newRow++;
      if (e.key === "ArrowLeft") newCol--;
      if (e.key === "ArrowRight") newCol++;

      // Bounds check
      if (
        newRow < 0 ||
        newCol < 0 ||
        newRow >= maze.length ||
        newCol >= maze[0].length
      ) {
        setMessage("Out of bounds!");
        return;
      }

      const tile = maze[newRow][newCol];

      // Wall or locked door check
      if (tile === "W") {
        setMessage("Blocked by wall!");
        return;
      }
      if (tile === "D" && !hasKey) {
        setMessage("The door is locked. You need a key!");
        return;
      }

      // Update position first
      setPosition([newRow, newCol]);

      // Record the move immediately
      if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(e.key)) {
        setMoves((prev) => {
          const newMoves = [...prev, e.key];
          console.log(newMoves);
          return newMoves;
        });
      }

      // Portal check
      if (tile === "P1") {
        const destinationCoords = findPortal(maze, "P2");
        setPosition(destinationCoords);
        setMessage("Teleported to P2!");
        return;
      }
      if (tile === "P2") {
        const destinationCoords = findPortal(maze, "P1");
        setPosition(destinationCoords);
        setMessage("Teleported to P1!");
        return;
      }

      // Key check
      if (tile === "K" && !hasKey) {
        setHasKey(true);
        setMessage("You collected the key!");
      }

      // Goal check
      if (tile === "G") {
        setMessage("You reached the goal!");
        submitMoves([...moves, e.key]);
      }

      // Reset message for normal tiles
      if (tile !== "K" && tile !== "G") {
        setMessage("");
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [position, hasKey, maze, moves]);

  const submitMoves = async (movesToSubmit) => {
    try {
      const response = await fetch(
        `http://localhost:8000/mazes/${mazeId}/verify`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ moves: movesToSubmit }),
        }
      );
      const result = await response.json();
      setMessage(result.message);
    } catch (err) {
      console.error("Error submitting moves:", err);
      setMessage("Failed to verify maze");
    }
  };

  return (
    <div>
      <div>
        {maze.map((row, rowIndex) => (
          <div key={rowIndex}>
            {row.map((cell, colIndex) => (
              <Tile
                key={colIndex}
                cell={cell}
                isPlayer={position[0] === rowIndex && position[1] === colIndex}
              />
            ))}
          </div>
        ))}
      </div>

      <p>{message}</p>
      <p>Use arrow keys to move</p>
      {hasKey ? <p>Key collected</p> : null}
    </div>
  );
};

export default MazeGame;
