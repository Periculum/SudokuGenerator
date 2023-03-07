#!/usr/bin/env python3

import random
import svgwrite

class Sudoku:
    def __init__(self, board):
        self.board = board
        
    def toSVG(self):
        cell_size = 40

        svg = svgwrite.Drawing('sudoku.svg', size = (9 * cell_size, 9 * cell_size))
        svg.add(svg.rect(insert = (0, 0), fill = 'white'))

        # Draw the grid lines
        for i in range(10):
            line_color = 'black'
            line_width = 2 if i % 3 == 0 else 0.5
            # row lines
            svg.add(svg.line(start = (i * cell_size, 0), end = (i * cell_size, 9 * cell_size),
                             stroke = line_color, stroke_width = line_width))
            # column lines
            svg.add(svg.line(start = (0, i * cell_size), end = (9 * cell_size, i * cell_size),
                             stroke = line_color, stroke_width = line_width))

        # Draw the numbers
        for row in range(9):
            for column in range(9):
                if self.board[row][column] != 0:
                    text = svg.text(str(self.board[row][column]), insert = ((column + 0.5) * cell_size,
                                                                        (row + 0.5) * cell_size),
                                    font_size = 20, font_family = 'Arial', text_anchor = 'middle', dominant_baseline = 'middle')
                    svg.add(text)

        svg.save()

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
    sudoku.toSVG()
    sudoku.print()


if __name__ == "__main__":
    main()
