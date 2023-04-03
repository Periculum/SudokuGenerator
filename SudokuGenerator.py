#!/usr/bin/env python3

import random
import sys
import time
from datetime import datetime

class Sudoku:
    def __init__(self):
        self.reset()

    def reset(self):
        # create empty 9x9 board
        rows = 9
        columns = 9
        self.board = [[0 for j in range(columns)] for i in range(rows)]


    def toSVG(self):
        # Variables
        cell_size = 40
        line_color = "black"

        # creating a rectangle in white with the size of a 9x9-Sudoku
        svg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">'
        svg += f'<rect x="0" y="0" width="{9 * cell_size}" height="{9 * cell_size}" fill="white" />'

        # Draw the grid lines
        for i in range(10):
            line_width = 2 if i % 3 == 0 else 0.5
            # row lines
            svg += f'<line x1="{i * cell_size}" y1="0"  x2="{i * cell_size}" y2="{9 * cell_size}" \
                            style="stroke:{line_color}; stroke-width:{line_width}" />'
            # column lines
            svg += f'<line x1="0" y1="{i * cell_size}"  x2="{9 * cell_size}" y2="{i * cell_size}" \
                            style="stroke:{line_color}; stroke-width:{line_width}" />'

        # Draw the numbers
        for row in range(9):
            for column in range(9):
                if self.board[row][column] != 0:
                    svg += f'<text x="{(column + 0.5) * cell_size}" y="{(row + 0.5) * cell_size}" \
                                    style="font-size:20; text-anchor:middle; dominant-baseline:middle"> {str(self.board[row][column])} </text>'

        svg += '</svg>'
        return svg

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

        # creating a list of coordinates to visit and shuffeling them
        unvisited = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(unvisited)

        # remove numbers
        while empty_cells > 0 and len(unvisited) > 0:
            # saving a copy of the number, just in case, if we cant remove it
            r, c = unvisited.pop()
            copy = self.board[r][c]
            self.board[r][c] = 0

            # checking how many solutions are in the board
            solutions = [solution for solution in self.solve()]

            # if there is more than one solution, we put the number back
            if len(solutions) > 1:
                self.board[r][c] = copy
            else:
                empty_cells -= 1

        # if unvisited is empty, but empty_cells not -> trying again
        if empty_cells > 0:
            print("No Sudoku found. Trying again.")
            return False
        else:
            return True




    def evaluate(self, difficulty):
        # 1 = really easy, 3 = middle, 6 = devilish (lowest number possible, takes a long time to calculate)
        empty_cells = [0, 25, 35, 45, 52, 58, 64]
        if difficulty < 1 or difficulty > len(empty_cells)-1:
            print("invalid difficulty", file=sys.stderr)
        return empty_cells[difficulty]


    # method to print the board in console
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
                    return
        yield True


def main():
    # takes difficulty as an argument, if not provided the program removes half of the board (level 3)
    args = [int(x) if x.isdecimal() else x for x in sys.argv[1:]]
    difficulty = args[0] if len(args) > 0 else 3

    sudoku = Sudoku()

    # trying in Total for 10 mins to find a sudoku
    timeout = 600
    start_time = time.time()
    end_time = start_time + timeout

    while time.time() < end_time:
        if sudoku.generate(difficulty) == True:
            break
        else:
            sudoku.reset()

    # printing
    sudoku.print()

    # creating the .svg-File with crrent date, time and difficulty
    svg = sudoku.toSVG()
    now = datetime.now()
    name = f'sudoku-{now:%Y%m%dT%H%M%S}-{difficulty}.svg'
    with open(name, 'w') as f:
        f.write(svg)


if __name__ == "__main__":
    main()
