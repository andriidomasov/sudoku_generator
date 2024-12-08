from flask import Flask, request, render_template
import random

app = Flask(__name__)


def is_valid_entry(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def fill_sudoku(board):
    """Fill the Sudoku board using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid_entry(board, row, col, num):
                        board[row][col] = num
                        if fill_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_sudoku():
    """Generate a random completed Sudoku board."""
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_sudoku(board)
    return board


def hide_fields(board, hidden_per_box):
    """Create a Sudoku puzzle by hiding fields."""
    puzzle = [row[:] for row in board]  # Copy the board
    for box_row in range(3):
        for box_col in range(3):
            cells = [(r, c) for r in range(box_row * 3, box_row * 3 + 3)
                     for c in range(box_col * 3, box_col * 3 + 3)]
            random.shuffle(cells)
            for i in range(hidden_per_box):
                row, col = cells[i]
                puzzle[row][col] = " "
                board[row][col] *= -1
    return puzzle


@app.route("/", methods=["GET", "POST"])
def index():
    sudoku_solution = None
    sudoku_puzzle = None
    if request.method == "POST":
        hidden_per_square = int(request.form.get("hidden_per_square", 0))

        # Generate Sudoku solution and puzzle
        sudoku_solution = generate_sudoku()
        sudoku_puzzle = hide_fields(sudoku_solution, hidden_per_square)

    return render_template(
        "index.html",
        solution=sudoku_solution,
        puzzle=sudoku_puzzle
    )


if __name__ == "__main__":
    app.run()
