import random as r
from string import ascii_uppercase
from fpdf import FPDF


# gets input from the user, hashed code can be used for testing/debug to auto input
def user_input():
    name = input("Title: ")
    # name = 'search'  # auto name
    # size = ['auto']
    size = input("Dimensions (x, y): ").replace(' ', '').split(',')
    if size == ['auto']:
        size = (20, 20)
    else:
        size = tuple(int(s) for s in size)
    words = input("Word bank, separated by commas: ").replace(' ', '').upper().split(',')
    # words = ['blue', 'purple', 'red', 'green', 'orange', 'yellow', 'cyan', 'violet']  # auto input
    return words, name, size


# generates a game board from the word arrays and desired size
def generate(words, size):
    puzzle = [[' ' for col in range(size[0])] for row in range(size[1])]  # creates empty game board
    for word in words:  # puts each word array onto the game board
        direction = (0, 0)
        while direction == (0, 0):
            direction = (r.randint(-1, 1), r.randint(-1, 1))  # chooses random (x, y) direction, can't be (0, 0)
        while True:  # emulates Do-while loop
            coords = (  # generates random starting coords that keep the word array in the bound of the game board
                r.randrange(
                    len(word) - 1 if direction[0] == -1 else 0,  # lower bound x
                    len(puzzle[0]) + 1 - len(word) if direction[0] == 1 else len(puzzle[0])),  # upper bound x
                r.randrange(
                    len(word) - 1 if direction[1] == -1 else 0,  # lower bound y
                    len(puzzle) + 1 - len(word) if direction[1] == 1 else len(puzzle))  # upper bound y
                )
            if all(puzzle[coords[1] + i * direction[1]][coords[0] + i * direction[0]] == ' '
                   for i, char in enumerate(word)):  # checks that no letters will be overwritten, and breaks if true
                break
        for i, char in enumerate(word):
            puzzle[coords[1] + i * direction[1]][coords[0] + i * direction[0]] = char  # draws word
    pre_puzzle = [row.copy() for row in puzzle]  # creates a deep copy of the puzzle
    for row, row_chars in enumerate(puzzle):  # fills empty spaces with random letters
        for col, char in enumerate(row_chars):
            if char == ' ':
                puzzle[row][col] = r.choice(list(ascii_uppercase))
    return puzzle, pre_puzzle


# formats the puzzle onto a pdf and outputs a .pdf file
def to_pdf(puzzle, name, size, words):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_left_margin(21)
    pdf.set_right_margin(21)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, name, 0, 2, 'C')
    pdf.ln(15)
    pdf.set_font_size(10)
    spacing = 168 / size[0]
    for row, row_chars in enumerate(puzzle):  # writes word search onto pdf
        for col, char in enumerate(row_chars):
            pdf.cell(spacing, 0, char, 0, 0, 'C')
        pdf.ln(spacing)
    pdf.ln(4)
    pdf.cell(0, 10, "WORD BANK", 0, 2, 'C')
    pdf.ln(4)
    for i, word in enumerate(words):  # creates word bank
        pdf.cell(42, 0, word, 0, 0, 'C')
        if i % 4 == 3:
            pdf.ln(6)
    pdf.output(f'{name}.pdf', 'F')


def main():
    words_list, puzzle_name, puzzle_size = user_input()
    while True:
        puzzle_array, puzzle_preview = generate(words_list, puzzle_size)
        for i in range(puzzle_size[1]):  # Outputs each list in the array as a string
            print('  '.join(puzzle_preview[i]))
        if input("Acceptable? (y/n) ") != 'n':
            break
    to_pdf(puzzle_array, puzzle_name, puzzle_size, words_list)


if __name__ == '__main__':
    main()
