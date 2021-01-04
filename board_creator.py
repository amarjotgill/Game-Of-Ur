import json
import tkinter as tk
from board_square import BoardSquare
from tkinter.filedialog import asksaveasfilename, askopenfile, LoadFileDialog, SaveFileDialog


class BoardSquarePlus:
    def __init__(self, x: int, y: int, label: tk.Label, entrance="", _exit="", rosette=False, forbidden=False):
        self.label = label
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = tk.StringVar(label.master, value=_exit)
        self.entrance = tk.StringVar(label.master, value=entrance)
        self.rosette = tk.BooleanVar(label.master, value=rosette)
        self.forbidden = tk.BooleanVar(label.master, value=forbidden)


class BoardCreatorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x800')
        self.title('Royal Game of Ur Board Creator')
        self.setup_main_menu()
        self.the_grid = self.create_grid()
        self.current_selection = None
        self.base_color = 'pale green'
        self.dimensions = {}

    def save_map(self):
        file_name = asksaveasfilename(title='Select File to save as map', filetypes=(('Royal Ur Files', '*.ur'),))
        if not file_name:
            return
        with open(file_name, 'w') as json_file:
            dict_grid = []
            for i in range(len(self.the_grid)):
                dict_grid.append([])
                for j in range(len(self.the_grid[i])):
                    bs = BoardSquare(i, j, self.the_grid[i][j].entrance.get(),
                                     self.the_grid[i][j].exit.get(),
                                     self.the_grid[i][j].rosette.get(),
                                     self.the_grid[i][j].forbidden.get())

                    bs.next_white = self.the_grid[i][j].next_white
                    bs.next_black = self.the_grid[i][j].next_black

                    dict_grid[i].append(bs.jsonify())

            json_file.write(json.dumps(dict_grid))

    def setup_main_menu(self):
        main_menu = tk.Menu()
        file_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label='Load Map', command=None)
        file_menu.add_command(label='Save Map', command=self.save_map)
        file_menu.add_command(label='Exit', command=None)
        grid_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label="Grid", menu=grid_menu)
        grid_menu.add_command(label="Set Dimensions", command=self.set_dimensions)
        self['menu'] = main_menu

    def set_dimensions(self):
        dimension_dialog = tk.Toplevel()
        tk.Label(dimension_dialog, text="Number of Rows: ").grid(row=0, column=0)
        tk.Label(dimension_dialog, text="Number of Cols: ").grid(row=1, column=0)

        rows_entry = tk.Entry(dimension_dialog, width=20)
        rows_entry.grid(row=0, column=1)

        cols_entry = tk.Entry(dimension_dialog, width=20)
        cols_entry.grid(row=1, column=1)

        self.dimensions['rows'] = rows_entry
        self.dimensions['cols'] = cols_entry

        tk.Button(dimension_dialog, text="Set", command=self.reset_dimensions).grid(row=2, column=0)
        tk.Button(dimension_dialog, text="Quit", command=dimension_dialog.destroy).grid(row=2, column=1)


    def reset_dimensions(self):
        rows = int(self.dimensions['rows'].get())
        cols = int(self.dimensions['cols'].get())
        self.destroy_grid()
        self.the_grid = self.create_grid(rows, cols)

    def destroy_grid(self):
        for i in range(len(self.the_grid)):
            for j in range(len(self.the_grid[i])):
                self.the_grid[i][j].label.grid_forget()
        self.the_grid = None

    def create_grid(self, rows=8, columns=3):
        the_grid = []
        for i in range(rows):
            the_grid.append([])
            for j in range(columns):
                the_label = tk.Label(self, text="({}, {})".format(i, j), height=6, width=12, borderwidth=2, relief="ridge", background='pale green')
                the_board_square = BoardSquarePlus(i, j, the_label)
                the_label.grid(row=i, column=j)
                the_label.bind("<Button-1>", lambda event, x=i, y=j: self.select_next(x, y, event))
                the_label.bind("<Button-3>", lambda event, x=i, y=j: self.label_click(x, y, event))
                the_grid[i].append(the_board_square)
        return the_grid

    def select_next(self, i, j, event):
        print('{} next selected ({}, {})'.format(self.current_selection, i, j))
        if not self.current_selection:
            return
        x, y = self.current_selection
        if self.next_color == 'white':
            self.the_grid[x][y].next_white = self.the_grid[i][j]
        else:
            self.the_grid[x][y].next_black = self.the_grid[i][j]
        self.current_selection = None

    def start_select_next_white(self, i, j):
        self.current_selection = (i, j)
        self.next_color = 'white'
        print('started select next on ({}, {})'.format(i, j))

    def start_select_next_black(self, i, j):
        self.current_selection = (i, j)
        self.next_color = 'black'
        print('started select next on ({}, {})'.format(i, j))

    def label_click(self, i, j, event):
        print(i, j)

        the_popup_menu = tk.Menu(self, tearoff=0)
        the_popup_menu.add_command(label="Do nothing")
        the_popup_menu.add_command(label="Select Next White", command=lambda x=i, y=j: self.start_select_next_white(x, y))
        the_popup_menu.add_command(label="Select Next Black", command=lambda x=i, y=j: self.start_select_next_black(x, y))
        the_popup_menu.add_checkbutton(label='Toggle Forbidden', onvalue=True, offvalue=False, variable=self.the_grid[i][j].forbidden,
                                       command=lambda: self.toggle_forbidden(i, j))
        the_popup_menu.add_checkbutton(label='Toggle Rosette', onvalue=True, offvalue=False, variable=self.the_grid[i][j].rosette,
                                       command=lambda: self.toggle_rosette(i, j))
        start_menu = tk.Menu(self, tearoff=0)
        start_menu.add_checkbutton(label='White Player Start', onvalue="White", offvalue="", variable=self.the_grid[i][j].entrance)
        start_menu.add_checkbutton(label='Black Player Start', onvalue="Black", offvalue="", variable=self.the_grid[i][j].entrance)
        end_menu = tk.Menu(self, tearoff=0)
        end_menu.add_checkbutton(label='Player White Exit', onvalue="White", offvalue="", variable=self.the_grid[i][j].exit)
        end_menu.add_checkbutton(label='Player Black Exit', onvalue="Black", offvalue="", variable=self.the_grid[i][j].exit)
        the_popup_menu.add_cascade(label="Entrance", menu=start_menu)
        the_popup_menu.add_cascade(label="Exit", menu=end_menu)
        the_popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def toggle_rosette(self, x, y):
        self.the_grid[x][y].forbidden.set(False)
        if self.the_grid[x][y].rosette.get():
            self.the_grid[x][y].label['background'] = 'gold'
        else:
            self.the_grid[x][y].label['background'] = self.base_color

    def toggle_forbidden(self, x, y):
        self.the_grid[x][y].rosette.set(False)
        if self.the_grid[x][y].forbidden.get():
            self.the_grid[x][y].label['background'] = 'tomato'
        else:
            self.the_grid[x][y].label['background'] = self.base_color


if __name__ == '__main__':
    bcw = BoardCreatorWindow()
    bcw.mainloop()
