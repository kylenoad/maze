import React, { useState } from "react";
import MazeGame from "./Maze";

const Dashboard = () => {
  const [selectedMazeId, setSelectedMazeId] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.reload();
  };

  return (
    <div>
      <h1>Maze Dashboard</h1>
      <button onClick={handleLogout}>Logout</button>
      <div>
        <button onClick={() => setSelectedMazeId(1)}>Maze 1</button>
        <button onClick={() => setSelectedMazeId(2)}>Maze 2</button>
      </div>

      {selectedMazeId && <MazeGame mazeId={selectedMazeId} />}
    </div>
  );
};

export default Dashboard;
