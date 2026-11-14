import time
import signal
import matplotlib.pyplot as plt
from sudoku import random_grid, backtrack_sudoku, backtrack_sudoku_mrv

TIMEOUT_SECONDS = 30


class TimeoutException(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutException()


# Register the 30-second alarm handler (works on macOS/Linux)
signal.signal(signal.SIGALRM, _timeout_handler)


def run_with_timeout(solver_func, grid, timeout=TIMEOUT_SECONDS):
    """Run a Sudoku solver with a strict timeout in seconds."""
    signal.alarm(timeout)
    start_time = time.time()
    try:
        solved = solver_func(grid)
        elapsed = time.time() - start_time
        signal.alarm(0)  # Cancel alarm if finished early
        return solved, elapsed
    except TimeoutException:
        return False, float(timeout)


simple_times = []
mrv_times = []
num_puzzles = 5

print(f"Running benchmark on {num_puzzles} random puzzles (30s timeout per solver)...")

for i in range(1, num_puzzles + 1):
    puzzle = random_grid(fill_prob=0.4)
    print(f"\nPuzzle {i}:")

    # 1. Simple Backtracking
    grid1 = [row[:] for row in puzzle]
    solved1, t1 = run_with_timeout(backtrack_sudoku, grid1)
    status1 = "Solved" if solved1 else "Timed out / Unsolvable"
    print(f"  Simple Backtracking: {t1:.4f}s ({status1})")
    simple_times.append(t1)

    # 2. MRV Backtracking
    grid2 = [row[:] for row in puzzle]
    solved2, t2 = run_with_timeout(backtrack_sudoku_mrv, grid2)
    status2 = "Solved" if solved2 else "Timed out / Unsolvable"
    print(f"  MRV Backtracking:    {t2:.4f}s ({status2})")
    mrv_times.append(t2)

x = list(range(1, num_puzzles + 1))

plt.figure(figsize=(10, 6))
plt.plot(x, simple_times, label="Simple Backtracking", color="purple", marker='o')
plt.plot(x, mrv_times, label="MRV Backtracking", color="pink", marker='s', linestyle='--')
plt.title("Compare MRV Backtrack and Simple Backtrack (30s Timeout Cap)")
plt.xlabel("Sudoku Puzzle Index")
plt.ylabel("Time Taken (seconds)")
plt.xticks(x)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.savefig("sudoku_mrv_comparison.png", dpi=300, bbox_inches="tight")
plt.show()