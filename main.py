from tkinter import Tk, Label, Canvas, messagebox
import pyglet
from ctypes import windll

# Player configs:
player_1 = {"symbol": "X", "colour": "red", "name": "player 1"}
player_2 = {"symbol": "O", "colour": "blue", "name": "player 2"}
current_player = None
past_symbols = []
past_coordinates = []

# Dimensions of tic-tac-toe grid:
rows = 3
columns = 3
width = 800
height = 800

# To fix blurry tkinter font. Taken from https://stackoverflow.com/questions/41315873/attempting-to-resolve-
# blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp/43046744#43046744
windll.shcore.SetProcessDpiAwareness(1)

# Rendering custom fonts. Taken from https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
pyglet.font.add_file('./fonts/arcadeclassic/ARCADECLASSIC.TTF')


# Coordinates of possible places to put X or O
coordinates = [(70, 160), (335, 160), (600, 160),
              (70, 440), (335, 440), (600, 440),
              (70, 700), (335, 700), (600, 700)]


def draw_grid(canv, w, h, rw, clm):
    cell_width = w // clm
    cell_height = h // rw

    # Creates the horizontal lines:
    for i in range(1, rw):
        # First two args are starting coordinates in x, y format, other two args are ending coordinates in same format.
        canv.create_line(0, i * cell_height, w, i * cell_height, fill="black")

    # Creates the vertical lines:
    for j in range(1, clm):
        canv.create_line(j * cell_width, 0, j * cell_width, h, fill="black")


def check_win(player_symbol):
    win_combinations = [
        [(70, 160), (335, 160), (600, 160)],   # Top row
        [(70, 440), (335, 440), (600, 440)],   # Middle row
        [(70, 700), (335, 700), (600, 700)],   # Bottom row
        [(70, 160), (70, 440), (70, 700)],     # Left column
        [(335, 160), (335, 440), (335, 700)],  # Middle column
        [(600, 160), (600, 440), (600, 700)],  # Right column
        [(70, 160), (335, 440), (600, 700)],   # Diagonal from top-left to bottom-right
        [(600, 160), (335, 440), (70, 700)]    # Diagonal from top-right to bottom-left
    ]

    for combination in win_combinations:
        # If all win coordinates are satisfied for that combination:
        all_points_present = True
        for point in combination:
            if point not in past_coordinates:
                all_points_present = False
                break

        if all_points_present:
            # symbols variable will be populated with the symbol of the label in the winning combination
            # symbols elements are either X or O
            symbols = []
            for coords in past_coordinates:
                if coords in combination:

                    # Obtains the symbol of the label at that coordinates:
                    index = past_coordinates.index(coords)
                    symbol = past_symbols[index]
                    symbols.append(symbol)

            if symbols.count(player_symbol) == 3:
                return True

    return False


def on_click(event):
    global current_player, past_symbols, past_coordinates

    for x_coord, y_coord in coordinates:
        point = (x_coord, y_coord)

        if x_coord - 125 < event.x < x_coord + 125 and y_coord - 125 < event.y < y_coord + 125:
            # If player 1 previously took a turn:
            if current_player == player_1:
                current_player = player_2
            # If player 2 previously took a turn OR it is the start of the game:
            elif current_player == player_2 or current_player is None:
                current_player = player_1

            player_move = Label(text=current_player["symbol"],
                                font=("ArcadeClassic", 120, "normal"),
                                fg=current_player["colour"])
            player_move.place(x=x_coord, y=y_coord)

            # Saves past moves and removes the move made from the possible moves left:
            past_symbols.append(player_move.cget("text"))
            past_coordinates.append(point)
            coordinates.remove(point)

            has_won = check_win(current_player["symbol"])
            if has_won is True:
                print(f"{current_player['name'].title()} won!")
                canvas.bind("<Button-1>", useless_function)
                message = messagebox.showinfo(title=f"{current_player['name'].title()} won!",
                                              message=f"Congratulations! {current_player['name'].title()} "
                                                      f"(using {current_player['symbol']}) won!")

            elif has_won is False and len(past_symbols) == 9:
                message = messagebox.showinfo(title="Oh no...",
                                              message="Nobody wins :( ")

            break


# This function does nothing and simply stops mouse clicking when someone wins.
def useless_function(event):
    pass


window = Tk()

window.title("Tic Tac Toe Game")
window.minsize(width=800, height=1000)
window.config(padx=20, pady=20)

# Render label title:
title_label = Label(text="Tic  Tac  Toe!", font=("ArcadeClassic", 50, "underline"), fg="purple")
title_label.config(pady=30)
title_label.grid(column=0, row=0)

# Canvas configs:
canvas = Canvas(width=width, height=height)
draw_grid(canvas, width, height, rows, columns)

# Creates event object which triggers function when left mouse button (button 1) is clicked:
# The event object has attributes .x and .y to obtain coordinates where mouse was clicked.
canvas.bind("<Button-1>", on_click)
canvas.grid(column=0, row=1)

window.mainloop()
