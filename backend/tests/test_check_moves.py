from utils import check_moves
import pytest

def test_simple_path():
    grid = [
        [" ", "G"],
        [" ", " "]
    ]
    moves = ["ArrowRight"]
    assert check_moves(grid, moves) == "Maze completed successfully!"

def test_hit_wall():
    grid = [
        [" ", "W", "G"]
    ]
    moves = ["ArrowRight", "ArrowRight"]
    assert check_moves(grid, moves) == "Invalid move: Hit a wall"

def test_locked_door_without_key():
    grid = [
        [" ", "D", "G"],
        ["K", " ", " "]
    ]
    moves = ["ArrowRight"]
    assert check_moves(grid, moves) == "Invalid move: Door is locked"

def test_collect_key_and_open_door():
    grid = [
        [" ", "D", "G"],
        ["K", " ", " "]
    ]
    moves = ["ArrowDown", "ArrowRight", "ArrowUp", "ArrowRight"]
    assert check_moves(grid, moves) == "Maze completed successfully!"

def test_invalid_move():
    grid = [[" ", "G"]]
    moves = ["ArrowUp"]
    assert check_moves(grid, moves) == "Invalid move: Out of bounds"

def test_key_pickup_only_once():
    grid = [
        ["K", "K", "G"]
    ]
    moves = ["ArrowRight", "ArrowRight"]
    result = check_moves(grid, moves)
    assert result == "Maze completed successfully!"

def test_portal_usage():
    grid = [
        [" ", "P1", " "],
        ["P2", " ", "G"]
    ]
    moves = ["ArrowRight", "ArrowRight", "ArrowRight"]
    assert check_moves(grid, moves) == "Maze completed successfully!"

def test_not_reaching_goal():
    grid = [[" ", "G"]]
    moves = []
    assert check_moves(grid, moves) == "Did not reach the goal"