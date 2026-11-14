import random

DEFAULT_GRID = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

DOMAINS = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def random_grid(fill_prob=0.3):
    """Generate a random valid partial 9x9 Sudoku grid."""
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for row in range(9):
        for col in range(9):
            if random.random() < fill_prob:
                num = random.randint(1, 9)
                if is_valid(grid, row, col, num):
                    grid[row][col] = num
    return grid


def find_empty_cell(grid):
    """Select the next unassigned cell sequentially."""
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None


def is_valid(grid, row, col, number):
    """Check row, column, and 3x3 subgrid constraints."""
    if number in grid[row]:
        return False

    for r in range(9):
        if grid[r][col] == number:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if grid[r][c] == number:
                return False

    return True


def backtrack_sudoku(grid):
    """Solve Sudoku using standard chronological backtracking."""
    empty_cell = find_empty_cell(grid)
    if not empty_cell:
        return True

    row, col = empty_cell
    for number in DOMAINS:
        if is_valid(grid, row, col, number):
            grid[row][col] = number
            if backtrack_sudoku(grid):
                return True
            grid[row][col] = 0

    return False


def mrv_variable(grid):
    """Select the unassigned cell with Minimum Remaining Values (MRV heuristic)."""
    min_domain_size = float('inf')
    best_cell = None

    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                valid_values = [num for num in DOMAINS if is_valid(grid, row, col, num)]
                if len(valid_values) < min_domain_size:
                    min_domain_size = len(valid_values)
                    best_cell = (row, col)
                    if min_domain_size == 1:
                        return best_cell
    return best_cell


def backtrack_sudoku_mrv(grid):
    """Solve Sudoku using backtracking enhanced with the MRV heuristic."""
    empty_cell = mrv_variable(grid)
    if not empty_cell:
        return True

    row, col = empty_cell
    for number in DOMAINS:
        if is_valid(grid, row, col, number):
            grid[row][col] = number
            if backtrack_sudoku_mrv(grid):
                return True
            grid[row][col] = 0

    return False


def print_grid(grid):
    """Display the 9x9 Sudoku board cleanly."""
    for row in range(9):
        if row in (3, 6):
            print("-" * 21)
        for col in range(9):
            if col in (3, 6):
                print("| ", end="")
            val = grid[row][col]
            print(val if val != 0 else ".", end=" ")
        print()


if __name__ == "__main__":
    grid_copy = [row[:] for row in DEFAULT_GRID]
    print("Initial Sudoku Puzzle:")
    print_grid(grid_copy)
    if backtrack_sudoku_mrv(grid_copy):
        print("\nSolved Sudoku (MRV):")
        print_grid(grid_copy)