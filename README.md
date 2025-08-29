# About

A full-stack maze-solving game with user authentication, built using:

### Backend

- FastAPI REST API
- PostgreSQL database seeded with example mazes

### Frontend

- React app for user login, registration, and interactive maze gameplay

### Authentication

- JWT-based login system
- Tokens securely stored in `localStorage`

# Quick Start

### 1. Backend

Clone the repo and enter the backend folder:

```bash
git clone https://github.com/kylenoad/maze.git
cd maze/backend
```

Start the app (this will also seed the database automatically):

```bash
docker compose up --build
```

### 2. Frontend

Open a new terminal and start the frontend:

```bash
cd maze/frontend
npm install
npm start
```

# API Documentation

http://localhost:8000/docs

## API Endpoints

- `GET /` — Root endpoint (health check or welcome message)
- `GET /mazes` — Retrieve all mazes
- `GET /mazes/{maze_id}` — Retrieve a specific maze by ID
- `POST /mazes/{maze_id}/verify` — Submit a solution to verify a maze
- `POST /register` — Register a new user
- `POST /login` — Log in and receive JWT token

# Stopping the Application

```bash
docker compose down
```

# Future Feature: Leaderboard for Games

Unfortunately I was unable to oput together the leaderboard aspect of this takehome as I had limited time, and thre was a lot of ground to cover. This is what would need to be implimented:

### Database Changes

- Create a table to store game results:
  - `user_id`, `maze_id`, `moves_taken`, `time_taken`, `score`

### Backend Logic

- Endpoint to submit results when a user completes a maze.
- Endpoint to fetch leaderboard data:
  - Fastest times
  - Fewest moves

### Frontend / UI

- Leaderboard page or component to display rankings.

### Authentication / Authorization

- Only authenticated users can submit scores.

# Testing

I wrote tests for utility functions (e.g., check_moves). I have not implemented tests for authentication or protected endpoints yet.

To run the tests go into virtual environment:

```bash
source backend/venv/bin/activate
pytest
```

### Authentication & Registration

- Registering a new user stores a hashed password, not plain text.
- Duplicate usernames are rejected with status `400`.
- Valid credentials return a JWT token.
- Invalid username or password returns status `401`.

### Protected Routes

- Accessing `/mazes` or `/mazes/{id}` without a token returns status `401`.
- Accessing with a valid token returns expected data.

# Use of AI

I used AI to clarify concepts and debug specific parts of the project, especially around authentication. It also supported areas I was less familiar with, such as setting up CORS, configuring environment variables and dependencies, creating Docker and YAML configuration files, and scaffolding boilerplate.

# My approach

I started by implementing the core game mechanics in JavaScript, focusing on solving the game logic first. Initially, I hard-coded the mazes to get things moving quickly. Once the maze mechanics were working, I created a seed script to populate the database with a couple of mazes and then built endpoints to serve them to the frontend.

Next, I developed the frontend dashboard to display the mazes.

On the backend, I implemented logic to validate the moves. The frontend collects all valid key inputs and sends the array to the backend, where a function replays the moves to verify a successful attempt. If the attempt is successful, the user receives an on-screen message.

To protect maze endpoints and ensure only registered users can access them, I implemented token-based authentication.

To store passwords securely, I used passlib with the bcrypt algorithm so that passwords are hashed before storing in the database.

