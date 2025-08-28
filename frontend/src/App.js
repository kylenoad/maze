import React, { useState, useEffect } from "react";
import Dashboard from "./components/Dashboard";
import LoginForm from "./components/LoginForm";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return isLoggedIn ? (
    <Dashboard />
  ) : (
    <LoginForm onLogin={() => setIsLoggedIn(true)} />
  );
}

export default App;
