def check_moves(grid, moves):

    current_row = 0
    current_col = 0
    has_key = False

    directions = {
        "ArrowUp": (-1, 0),
        "ArrowDown": (1, 0),
        "ArrowLeft": (0, -1),
        "ArrowRight": (0, 1),
    }

    def find_portal(label):
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == label:
                    return r, c
        return current_row, current_col

    for move in moves:
    # Look up the change for this move
        change = directions[move]
        row_change = change[0]  
        col_change = change[1] 

        # Calculate the new position
        new_row = current_row + row_change
        new_col = current_col + col_change

        # Check if new position is outside the grid
        if new_row < 0 or new_row >= len(grid) or new_col < 0 or new_col >= len(grid[0]):
            return "Invalid move: Out of bounds"

        # Check what is in the new position
        tile = grid[new_row][new_col]

        # Check for wall
        if tile == "W":
            return "Invalid move: Hit a wall"

        # Check for locked door
        if tile == "D" and not has_key:
            return "Invalid move: Door is locked"

        # Pick up key if there is one
        if tile == "K":
            has_key = True

        # Go through portals
        if tile == "P1":
            current_row, current_col = find_portal("P2")
        elif tile == "P2":
            current_row, current_col = find_portal("P1")
        else:
            current_row = new_row
            current_col = new_col
            
        # Check goal
        if tile == "G":
            return "Maze completed successfully!"

    # Check if the player reached the goal
    if grid[current_row][current_col] == "G":
        return "Maze completed successfully!"
    else:
        return "Did not reach the goal"
