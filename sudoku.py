from tkinter import *
from tkinter import ttk
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class Sudoku(Frame):
    def __init__(self, root):
        self.parent = root

        self.parent.title("Sudoku")

        self.row = 0
        self.col = 0

        Frame.__init__(self, root)

        self.pack(fill=BOTH, expand=1)

        self.create_frame = ttk.Frame(self, width=WIDTH, height=HEIGHT)
        self.play_frame = ttk.Frame(self, width=WIDTH, height=HEIGHT)
        
        self.home()

    def home(self):
        self.home_frame = ttk.Frame(self, width=WIDTH, height=HEIGHT)
        self.home_frame.pack(fill=BOTH, expand=1)

        welcome_msg = ttk.Label(self.home_frame, text= 
            "Welcome to the sudoku solver\n"+
            "Press play to solve a Sudoku\n"+
            "Press create to create a custom sudoku and submit to solve it",
            justify='center'
        )
        welcome_msg.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.game = SudokuGame('filled')
        self.game.start()

        play_btn = ttk.Button(self.home_frame, text= 'Play a Game', command=self.play_puzzle)
        play_btn.grid(row = 1, column = 0, pady=10)

        create_btn = ttk.Button(self.home_frame, text='Create a Sudoku', command=self.create_puzzle)
        create_btn.grid(row=1, column=1, pady=10)

    def create_puzzle(self):
        self.home_frame.pack_forget()
        self.create_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.create_frame, width=WIDTH, height=HEIGHT)
        self.canvas.grid(row = 0, column = 0, columnspan=9, rowspan=9)

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

        self.game = SudokuGame('empty')
        self.game.start()

        self.draw_grid()

        submit_btn = ttk.Button(self.create_frame, text='Submit', command=self.goto_play)
        home_btn = ttk.Button(self.create_frame, text='Home', command=lambda: self.return_home('create'))
        submit_btn.grid(row= 1, column = 11)
        home_btn.grid(row = 3, column = 11)

    def play_puzzle(self):
        print('called')
        self.play_frame.pack_forget()
        self.home_frame.pack_forget()
        self.play_frame.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self.play_frame, width=WIDTH, height=HEIGHT)
        self.canvas.grid(row=0, column=0, columnspan=9, rowspan=9)

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

        solution_btn = ttk.Button(self.play_frame, text='Solution', command=self.solve_puzzle)
        home_btn = ttk.Button(self.play_frame, text='Home', command=lambda: self.return_home('play'))
        clear = ttk.Button(self.play_frame, text='clear', command = lambda: self.canvas.delete('numbers'))
        view_solution_btn = ttk.Button(self.play_frame, text='View Solution', command=self.view_solution)

        solution_btn.grid(row= 1, column = 11)
        home_btn.grid(row = 3, column = 11)
        clear.grid(row=5, column = 11)
        view_solution_btn.grid(row=7, column = 11)

        self.draw_grid()
        self.draw_puzzle()

    def view_solution(self):
        find = self.game.find_empty()
        if not find:
            print('Solution found')
            return True
        else:
            e_row, e_col = find

        for i in range(1,10):
            if self.game.is_valid(i, e_row, e_col):
                self.game.puzzle[e_row][e_col] = i
                
                self.play_puzzle()
                time.sleep(1)

                if self.view_solution():
                    return True

                self.game.puzzle[e_row][e_col] = 0
                # self.canvas.delete(number)

        return False

    def draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

        print('draw puzzle')

    def draw_grid(self):
        for i in range(10):
            color = 'blue' if i%3==0 else 'gray'
            
            x0 = MARGIN + i*SIDE
            y0 = MARGIN
            x1 = MARGIN + i*SIDE
            y1 = HEIGHT - MARGIN

            self.canvas.create_line(x0,y0,x1,y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i*SIDE
            x1 = WIDTH-MARGIN
            y1 = MARGIN + i*SIDE

            self.canvas.create_line(x0,y0,x1,y1, fill=color)

        print('draw grid')

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.start_puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.draw_cursor()

    def key_pressed(self, event):
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.draw_puzzle()
            self.draw_cursor()
            # if self.game.check_win():
            #     self.draw_victory()

    def draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1,outline="red", tags="cursor")

    def solve_puzzle(self):
        if self.game.solve():
            print(self.game.puzzle)
            self.draw_puzzle()
        else:
            print('no solution found')

    def goto_play(self):
        self.create_frame.pack_forget()

        self.play_puzzle()

    def return_home(self, origin):
        if origin == 'create':
            self.create_frame.pack_forget()

        elif origin == 'play':
            self.play_frame.pack_forget()

        self.home()

class SudokuBoard(object):
    def __init__(self, file):
        self.board = self.__create_board(file)

    def __create_board(self, file):
        with open(file) as board_file:
            board = []
            for line in board_file:
                line = line.strip()
                if len(line) != 9:
                    raise SudokuError("Each line in the sudoku puzzle must be 9 chars long.")
                board.append([])

                for c in line:
                    if not c.isdigit():
                        raise SudokuError("Valid characters for a sudoku puzzle must be in 0-9")
                    board[-1].append(int(c))

            if len(board) != 9:
                raise SudokuError("Each sudoku puzzle must be 9 lines long")
            return board

class SudokuGame(object):
    def __init__(self, board_type):
        # takes input of type of board and reads the respective type of puzzle 
        self.board_type = board_type
        if self.board_type == 'filled':
            self.start_puzzle = SudokuBoard('1.sudoku').board
        elif self.board_type == 'empty':
            self.start_puzzle = SudokuBoard('0.sudoku').board
        print(self.start_puzzle)

    def start(self):
        # This function initializes the puzzle into the puzzle variable
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            e_row, e_col = find

        for i in range(1,10):
            if self.is_valid(i, e_row, e_col):
                self.puzzle[e_row][e_col] = i

                if self.solve():
                    return True

                self.puzzle[e_row][e_col] = 0

        return False

    def is_valid(self, num, row, col):
        # Check Row
        for i in range(9):
            if self.puzzle[row][i] == num and col != i:
                return False

        # Check Column
        for i in range(9):
            if self.puzzle[i][col] == num and row != i:
                return False

        # Check Box
        box_x = col//3
        box_y = row//3

        for i in range(box_y*3, box_y*3+3):
            for j in range(box_x*3, box_x*3+3):
                if self.puzzle[i][j] == num and i != row and j != col:
                    return False

        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                # print(self.game.puzzle[i][j])
                if int(self.puzzle[i][j]) == 0:
                    return (i,j)

        return None

    def check_win(self):
        for i in range(9):
            for j in range(9):
                if not  self.is_valid(self.puzzle[i][j], i, j):
                    return False
            return True

if __name__ == "__main__":
    root = Tk()
    Sudoku(root)

    # root.geometry("%dx%d" %(WIDTH, HEIGHT+40))
    root.mainloop()