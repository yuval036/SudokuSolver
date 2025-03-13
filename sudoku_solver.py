import tkinter as tk
from tkinter import messagebox

SIZE= 9

class SudokuSolver:
    def __init__(self, root):
        self .root = root
        self .root.title("Sudoku Solver")
        self .cells=[[tk.Entry(root, width=3, font=("Arial", 18), justify="center") for _ in range(SIZE)] for _ in range(SIZE)]
        

        for row in range(SIZE):
            for col in range(SIZE):
                self .cells[row][col].grid(row=row, column=col, padx=3, pady=3)
                self.cells[row][col].bind("<KeyRelease>", self.validate_input)

                self.cells[row][col].bind("<Up>", lambda event, r=row, c=col: self.move_cursor(r - 1, c))
                self.cells[row][col].bind("<Down>", lambda event, r=row, c=col: self.move_cursor(r + 1, c))
                self.cells[row][col].bind("<Left>", lambda event, r=row, c=col: self.move_cursor(r, c - 1))
                self.cells[row][col].bind("<Right>", lambda event, r=row, c=col: self.move_cursor(r, c + 1))

                if col % 3 == 0 and col != 0:
                    self.cells[row][col].grid_configure(padx=(10, 3))
                if row % 3 == 0 and row != 0:
                    self.cells[row][col].grid_configure(pady=(10, 3))


        solve_button = tk.Button(root, text="Solve", command=self.solve_sudoku, font=("Arial", 14),bg="lightblue")
        solve_button.grid(row=SIZE, column=0, columnspan=SIZE//2, sticky="we")
        clear_button = tk.Button(root, text="Clear", command=self .clear_grid, font=("Arial", 14), bg="lightblue")
        clear_button.grid(row=SIZE, column=SIZE//2, columnspan=SIZE//2, sticky="we")

    def validate_input(self, event):
        value = event.widget.get()
        if value != "" and not value.isdigit():
            messagebox.showwarning("Invalid Input", "Please enter a number between 1 and 9.")
            event.widget.delete(0, tk.END)
        elif value != "" and not (1 <= int(value) <=9):
            messagebox.showwarning("Invalid Input", "Please enter a number between 1 and 9.")
            event.widget.delete(0, tk.END)

    def get_focus_position(self):
        for row in range(SIZE):
            for col in range(SIZE):
                if self.cells[row][col] == self.root.focus_get():
                    return row, col
        return None, None

    def move_cursor(self, row, col):
        if 0 <= row <SIZE and 0 <=col < SIZE:
            self.cells[row][col].focus_set()

    def get_board(self):
        board = []
        for row in range(SIZE):
            current_row = []
            for col in range(SIZE):
                value = self.cells[row][col].get()
                current_row.append(int(value) if value.isdigit() else 0)
            board.append(current_row)
        return board
    
    def set_board(self, board):
        for row in range(SIZE):
            for col in range(SIZE):
                self.cells[row][col].delete(0, tk.END)
                if board[row][col] !=0:
                    self.cells[row][col].insert(tk.END, str(board[row][col]))


    def solve_sudoku(self):
        board = self.get_board()
        if self.solve(board):
            self.set_board(board)
        else:
            messagebox.showerror("Error!, There is no solusion for this board.")

    def is_valid(self, board, row, col, num):
        for i in range(SIZE):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = (row//3) * 3, (col//3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row+i][start_col+j] == num:
                    return False
        return True
    
    def solve(self, board):
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == 0:
                    for num in range(1, SIZE+1):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

    def clear_grid(self):
        for row in range(SIZE):
            for col in range(SIZE):
                self.cells[row][col].delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()


    