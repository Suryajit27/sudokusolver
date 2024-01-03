import streamlit as st
import pandas as pd

def solve_sudoku(matrix):
    # Your Sudoku solving logic here (you can reuse the existing solve_sudoku function)
    empty = find_empty(matrix)
    if not empty:
        return matrix  # Puzzle solved

    row, col = empty

    for num in range(1, 10):
        if is_valid(matrix, row, col, num):
            matrix[row][col] = num

            if solve_sudoku(matrix):
                return matrix

            matrix[row][col] = 0  # Backtrack if the current configuration leads to failure

    return None  # No solution found

def is_valid(matrix, row, col, num):
    # Check if 'num' is not in the current row, column, or 3x3 square
    return (
        not used_in_row(matrix, row, num)
        and not used_in_column(matrix, col, num)
        and not used_in_square(matrix, row - row % 3, col - col % 3, num)
    )

def used_in_row(matrix, row, num):
    return num in matrix[row] and matrix[row].count(num) == 1

def used_in_column(matrix, col, num):
    return num in [matrix[i][col] for i in range(9)] and [matrix[i][col] for i in range(9)].count(num) == 1

def used_in_square(matrix, start_row, start_col, num):
    return any(
        matrix[i][j] == num and (i, j) != (start_row, start_col)
        for i in range(start_row, start_row + 3)
        for j in range(start_col, start_col + 3)
    )

def find_empty(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return (i, j)
    return None

def parse_input(input_df):
    return [[int(input_df.iloc[i, j]) if pd.notna(input_df.iloc[i, j]) and str(input_df.iloc[i, j]).isdigit() else 0 for j in range(9)] for i in range(9)]

def main():
    st.title("Sudoku Solver")

    st.write("Enter the Sudoku puzzle below (use 0 for empty cells):")

    # Create an editable dataframe for user input
    sudoku_input_df = pd.DataFrame([[0] * 9 for _ in range(9)], columns=[f"Col {i + 1}" for i in range(9)])
    edited_df = st.data_editor(sudoku_input_df)

    if st.button("Solve Sudoku"):
        # Parse the input dataframe into a Sudoku matrix
        input_matrix = parse_input(edited_df)
        result = solve_sudoku(input_matrix)

        if result is not None:
            st.write("\nSolved Sudoku puzzle:")
            st.table(pd.DataFrame(result, columns=[f"Col {i + 1}" for i in range(9)]))
        else:
            st.write("\nNo solution found for the given puzzle.")

if __name__ == "__main__":
    main()