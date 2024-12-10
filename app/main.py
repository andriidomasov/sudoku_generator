from flask import Flask, request, render_template
import random
from typing import List, Set, Tuple

app = Flask(__name__)


def is_valid_entry(board: List[List[int]], row: int, col: int, num: int) -> bool:
    """Check if placing num in board[row][col] is valid."""
    # Early row check
    if num in board[row]:
        return False
    
    # Early column check using set comprehension for better performance
    if num in {board[i][col] for i in range(9)}:
        return False
    
    # Box check with range limiting
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    return True


def get_empty_cell(board: List[List[int]]) -> Tuple[int, int]:
    """Find the next empty cell in the board."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1


def fill_sudoku(board: List[List[int]]) -> bool:
    """Fill the Sudoku board using backtracking."""
    row, col = get_empty_cell(board)
    if row == -1 and col == -1:  # Board is filled
        return True
        
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid_entry(board, row, col, num):
            board[row][col] = num
            if fill_sudoku(board):
                return True
            board[row][col] = 0
    return False


def generate_sudoku() -> List[List[int]]:
    """Generate a random completed Sudoku board."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    # Initialize with some random numbers to speed up generation
    for _ in range(17):  # Minimum clues needed for unique solution
        row, col = random.randrange(9), random.randrange(9)
        if board[row][col] == 0:
            nums = list(range(1, 10))
            random.shuffle(nums)
            for num in nums:
                if is_valid_entry(board, row, col, num):
                    board[row][col] = num
                    break
    fill_sudoku(board)
    return board


def hide_fields(board: List[List[int]], hidden_per_box: int) -> List[List[int]]:
    """Create a Sudoku puzzle by hiding fields strategically."""
    puzzle = [row[:] for row in board]
    boxes = [(i, j) for i in range(3) for j in range(3)]
    random.shuffle(boxes)  # Randomize box order
    
    for box_row, box_col in boxes:
        cells = [(r, c) for r in range(box_row * 3, box_row * 3 + 3)
                 for c in range(box_col * 3, box_col * 3 + 3)]
        random.shuffle(cells)
        for i in range(min(hidden_per_box, len(cells))):
            row, col = cells[i]
            puzzle[row][col] = " "
            board[row][col] = board[row][col] * -1
    return puzzle


@app.route("/", methods=["GET", "POST"])
def index():
    sudoku_solution = None
    sudoku_puzzle = None
    if request.method == "POST":
        hidden_per_square = int(request.form.get("hidden_per_square", 0))
        sudoku_solution = generate_sudoku()
        sudoku_puzzle = hide_fields(sudoku_solution, hidden_per_square)

    return render_template(
        "index.html",
        solution=sudoku_solution,
        puzzle=sudoku_puzzle
    )


if __name__ == "__main__":
    app.run()
