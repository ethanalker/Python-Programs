import random as r
from string import ascii_uppercase
from fpdf import FPDF


# gets input from the user, hashed code can be used for testing/debug to auto input
def user_input():
    name = input('Title: ')
    # name = 'search'  # auto name
    size = input('Dimensions: ').replace(' ', '').split(',')
    if size == ['auto']:
        size = (20, 20)
    else:
        size = tuple(int(s) for s in size)
    words = input("Word bank, separated by commas: ").replace(' ', '').upper().split(',')
    # words = ['blue', 'purple', 'red', 'green', 'orange', 'yellow', 'cyan', 'violet']  # auto input
    return words, name, size


# stores each word into an array such that each word array can be placed onto the puzzle array
# each word can face in one of eight random directions
def words_to_array(words):
    array_list = []
    for word in words:
        direction = (0, 0)
        coor = [0, 0]
        while direction == (0, 0):
            direction = (r.randint(-1, 1), r.randint(-1, 1))  # chooses random (x, y) direction, can't be (0, 0)
        array = [[' '] if direction[0] == 0 else [' ' for col in word] for row in word]  # creates empty array
        if direction[1] == 0:  # resizes array to fit word more snugly
            array = array[:1]
        elif direction[1] == -1:  # chooses coords to start drawing the word at based on direction
            coor[1] = len(word) - 1
        if direction[0] == -1:
            coor[0] = len(word) - 1
        for i, char in enumerate(word):
            array[coor[1] + i * direction[1]][coor[0] + i * direction[0]] = char  # draws word
        array_list.append(array)  # appends word array to a lists of arrays
    return array_list


# generates a game board from the word arrays and desired size
def generate(arrays, size):
    puzzle = [[' ' for col in range(size[0])] for row in range(size[1])]  # creates empty game board
    for array in arrays:  # puts each word array onto the game board
        while True:  # emulates Do-while loop
            coor = (  # generates random starting coords that keep the word array in the bound of the game board
                r.randrange(len(puzzle[0]) - len(array[0]) + 1), r.randrange(len(puzzle) - len(array) + 1))
            if all(all(char == ' ' or puzzle[coor[1] + row][coor[0] + col] == ' '
                       for col, char in enumerate(row_chars)) for row, row_chars in enumerate(array)):
                break  # checks that no letters will be overwritten, and breaks if true
        for row, row_chars in enumerate(array):  # draws non-empty elements of array onto game board
            for col, char in enumerate(row_chars):
                if char != ' ':
                    puzzle[coor[1] + row][coor[0] + col] = char
    for row, row_chars in enumerate(puzzle):  # fills empty spaces with random letters
        for col, char in enumerate(row_chars):
            if char == ' ':
                puzzle[row][col] = r.choice(list(ascii_uppercase))
    return puzzle


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
    padding = 168 / size[0]
    for row, row_chars in enumerate(puzzle):  # writes word search onto pdf
        for col, char in enumerate(row_chars):
            pdf.cell(padding, 0, char, 0, 0, 'C')
        pdf.ln(padding)
    pdf.ln(4)
    pdf.cell(0, 10, 'WORD BANK', 0, 2, 'C')
    pdf.ln(4)
    for i, word in enumerate(words):  # creates word bank
        pdf.cell(42, 0, word, 0, 0, 'C')
        if i % 4 == 3:
            pdf.ln(6)
    pdf.output(f'{name}.pdf', 'F')


def main():
    words_list, puzzle_name, puzzle_size = user_input()
    puzzle_array = generate(words_to_array(words_list), puzzle_size)
    to_pdf(puzzle_array, puzzle_name, puzzle_size, words_list)


if __name__ == "__main__":
    main()
