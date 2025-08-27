import React, { useState, useEffect } from "react";
import Tile from "./Tile";

const maze = [
  ["S", "W", "P2", "W", "W", "", "", "P1"],
  ["", "W", "K", "W", "", "", "", "W"],
  ["", "W", "W", "W", "", "W", "", "W"],
  ["", "W", "", "", "", "W", "", "W"],
  ["", "W", "", "W", "W", "W", "", "W"],
  ["", "", "", "W", "", "", "", "W"],
  ["", "W", "", "W", "", "W", "W", "W"],
  ["", "W", "", "W", "", "", "D", "G"],
];

const findPortal = (maze, portal) => {
  for (let row = 0; row < maze.length; row++) {
    for (let col = 0; col < maze[row].length; col++) {
      if (maze[row][col] === portal) return [row, col];
    }
  }
  return null;
};

const MazeGame = () => {
  const [position, setPosition] = useState([0, 0]);
  const [message, setMessage] = useState("");
  const [hasKey, setHasKey] = useState(false);

  useEffect(() => {
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
        newCol >= maze.length
      ) {
        setMessage("Out of bounds!");
        return;
      }

      const tile = maze[newRow][newCol];

      // Wall check
      if (tile === "W") {
        setMessage("Blocked by wall!");
        return;
      }

      // Door check
      if (tile === "D" && !hasKey) {
        setMessage("The door is locked. You need a key!");
        return;
      }

      // Check if the player is on a portal
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
      } else if (tile === "G") {
        setMessage("You reached the goal!");
      } else {
        setMessage("");
      }

      setPosition([newRow, newCol]);
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [position, hasKey]);

  return (
    <div>
      <h2>Maze</h2>

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
