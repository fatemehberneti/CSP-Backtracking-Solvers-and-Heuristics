def generate_magic_square(n):
    if n % 2 == 0:
        print("Magic squares are only possible for odd numbers.")
        return
    
    # Create an empty n x n grid
    magic_square = [[0] * n for _ in range(n)]
    
    # Start position for the first number (1)
    row, col = 0, n // 2
    
    # Fill the square with numbers 1 to n*n
    for num in range(1, n * n + 1):
        magic_square[row][col] = num
        
        # Move to the next position (top-right)
        new_row, new_col = (row - 1) % n, (col + 1) % n
        
        # If the new cell is already filled, move down instead
        if magic_square[new_row][new_col]:
            row += 1
        else:
            row, col = new_row, new_col
    
    # Print the magic square
    for row in magic_square:
        print(row)

# Example: Generate a 3x3 magic square
generate_magic_square(3)
