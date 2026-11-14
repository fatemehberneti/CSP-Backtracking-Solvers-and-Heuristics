def is_safe(queens, row, col):
    """
    Check if placing a queen at (row, col) is valid.
    """
    for r, c in enumerate(queens):
        if c == col or abs(r - row) == abs(c - col):
            return False
    return True

def solve_n_queens(n):
    """
    Solve the N-Queens problem using backtracking.
    """
    def backtrack(row, queens):
        if row == n:  # All queens placed
            return queens
        for col in range(n):
            if is_safe(queens, row, col):
                queens.append(col)  # Place queen
                result = backtrack(row + 1, queens)
                if result:
                    return result
                queens.pop()  # Backtrack
        return None

    return backtrack(0, [])  # Start with an empty board

def print_board(queens):
    """
    Print the board with queens placed.
    """
    if not queens:
        print("No solution exists!")
        return

    n = len(queens)
    for row in range(n):
        line = ["Q" if col == queens[row] else "." for col in range(n)]
        print(" ".join(line))

# Solve and display the 8 Queens solution
n = 8
solution = solve_n_queens(n)
print_board(solution)
