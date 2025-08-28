import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      const endpoint = isRegister ? "register" : "login";
      const response = await axios.post(`${API_URL}/${endpoint}`, {
        username,
        password,
      });

      if (!isRegister) {
        localStorage.setItem("token", response.data.access_token);
        onLogin();
      } else {
        setIsRegister(false);
        setMessage("Registration successful. Please login.");
      }
    } catch (err) {
      setMessage(err.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <div>
      <h2>{isRegister ? "Register" : "Login"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">{isRegister ? "Register" : "Login"}</button>
      </form>
      <button onClick={() => setIsRegister(!isRegister)}>
        {isRegister ? "Go to Login" : "Register"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default LoginForm;
