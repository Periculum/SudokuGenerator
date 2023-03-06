#!/usr/bin/env python3

import random

class Sudoku:
    def __init__(self, board):
        self.board = board

    def generate(self, difficulty):
        # fill diagonal squares
        for i in range(0, 9, 3):
            square = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(square)
            for r in range(3):
                for c in range(3):
                    self.board[r + i][c + i] = square.pop()

        # fill rest
        for solutions in self.solve():
            break

        # difficulty
        empty_cells = self.evaluate(difficulty)

        #remove numbers
        while(empty_cells > 0):
            r, c = random.randint(0, 8), random.randint(0, 8)
            if self.board[r][c] == 0:
                continue
            else:
                # saving a copy of the number, just in case, if we cant remove it
                copy = self.board[r][c]
                self.board[r][c] = 0

                # checking how many solutions are in the board
                solutions = [solution for solution in self.solve()]

                # if there is more than one solution, we put the number back
                if len(solutions) > 1:
                    self.board[r][c] = copy
                else:
                    empty_cells -= 1



    def evaluate(self, difficulty):
        # 1 = really easy, 3 = hard, 5 = nearly impossible
        if difficulty == 1:
            return 28
        elif difficulty == 2:
            return 39
        elif difficulty == 3:
            return 50
        elif difficulty == 4:
            return 60
        elif difficulty == 5:
            return 71
        else:
            print("Difficulty don't exist")


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
    # making an empty 9x9 board
    rows = 9
    column = 9
    board = [[0 for j in range(column)] for i in range(rows)]

    sudoku = Sudoku(board)
    sudoku.generate(3)
    sudoku.print()


if __name__ == "__main__":
    main()
