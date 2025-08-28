#Tests to write

# Registering a new user stores hashed password, not plain text

# Duplicate usernames are rejected with status 400

# Valid credentials return a JWT token

# Invalid username or password returns 401

# Accessing /mazes or /mazes/{id} without a token returns 401

# Accessing with a valid token returns expected data