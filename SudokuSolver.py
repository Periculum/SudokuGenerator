#!/usr/bin/env python3

class Sudoku:
    def __init__(self, board):
        self.board = board
        
    # evaluates the difficulty of the sudoku by counting the empty spaces
    def evaluate(self):
        empty_cells = sum(self.board, []).count(0)
        if empty_cells <= 28:
            return "Pretty easy"
        elif empty_cells <= 39:
            return "Easy"
        elif empty_cells <= 53:
            return "Medium"
        elif empty_cells <= 64:
            return "Hard"
        elif empty_cells <= 71:
            return "Pretty hard"
        else:
            return "Diabolical"


    # method to print the board
    def print(self):
        for i in range(9):
            print(" ".join([str(x)if x != 0 else "." for x in self.board[i]]))


    def number_is_valid(self, row, column, number):
        # check row and column
        for i in range(9):
            if self.board[row][i] == number or self.board[i][column] == number:
                return False

        # check square
        start_column = column // 3 * 3
        start_row = row // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_column] == number:
                    return False
        return True


    def solve(self):
        # find an empty cell
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    # for every empty cell fill a valid number into it
                    for n in range(1, 10):
                        if self.number_is_valid(r, c, n):
                            self.board[r][c] = n
                            # is it solved?
                            yield from self.solve()
                            # backtrack
                            self.board[r][c] = 0
                    return False
        yield True

def main():
    # example board, 4 possible Solutions
    board = [[0, 7, 6, 0, 1, 3, 0, 0, 0],
             [0, 4, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 8, 6, 9, 0, 7, 0, 0],
             [0, 5, 0, 0, 6, 9, 0, 3, 0],
             [0, 0, 0, 0, 0, 0, 5, 4, 0],
             [0, 8, 0, 7, 3, 0, 0, 0, 0],
             [5, 1, 0, 0, 2, 6, 8, 0, 0],
             [0, 0, 7, 1, 0, 0, 9, 0, 0],
             [0, 0, 0, 0, 4, 0, 0, 6, 0]]

    sudoku = Sudoku(board)
    print("Difficulty: " + sudoku.evaluate())

    # needed for multiple solutions
    counter = 0
    for solutions in sudoku.solve():
        print()
        sudoku.print()
        counter += 1
    print("Solutions: ", counter)


if __name__ == "__main__":
    main()
