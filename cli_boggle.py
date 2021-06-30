from Trie import Trie
from boggle_helper import solve_board
from blessed import Terminal
import time


class BoggleBoard:
    def __init__(self, size):
        self.SIZE = size

        self.board = [[" " for x in range(self.SIZE)]
                      for y in range(self.SIZE)]

        self.last_solution = []

        self.last_time = 999

        self.auto_refresh = True

    def solve(self, solver):
        start_time = time.time()
        self.last_solution = list(solver(self.board))

        self.last_solution.sort(key=len, reverse=True)

        elapsed = time.time() - start_time

        self.last_time = elapsed * 1000

    def clear_board(self):
        self.board = list([[" " for x in range(self.SIZE)]
                           for y in range(self.SIZE)])


class Cursor:
    def __init__(self, max_range):
        self.max_range = max_range

        self.x = 0
        self.y = 0

    def move_left(self):
        if self.x > 0:
            self.x -= 1
            return True
        return False

    def move_right(self):
        if self.x + 1 < self.max_range:
            self.x += 1
            return True
        return False

    def move_up(self):
        if self.y > 0:
            self.y -= 1
            return True
        return False

    def move_down(self):
        if self.y + 1 < self.max_range:
            self.y += 1
            return True
        return False


def echo(str):
    print(str, end="")


def render_entire_scene(boggle_board, cursor, term):
    vertical_line = "║"
    horizontal_line = "═"
    ul_corner = "╔"
    ur_corner = "╗"
    ll_corner = "╚"
    lr_corner = "╝"
    border_top = "╦"
    border_left = "╠"
    border_bot = "╩"
    border_right = "╣"
    junction = "╬"

    top_row = (border_top +
               3 * horizontal_line) * boggle_board.SIZE + ur_corner
    top_row = ul_corner + top_row[1:]

    bot_row = (border_bot +
               3 * horizontal_line) * boggle_board.SIZE + lr_corner
    bot_row = ll_corner + bot_row[1:]

    line_row = (junction +
                3 * horizontal_line) * boggle_board.SIZE + border_right
    line_row = border_left + line_row[1:]

    echo(term.home + term.clear + term.move_yx(0, 0))

    echo(top_row)
    for y in range(boggle_board.SIZE):

        echo(term.move_yx((2 * y) + 1, 0) + vertical_line + " ")

        for x in range(boggle_board.SIZE):
            ps = term.move_yx(1 + (y * 2), 1 + (4 * x))

            L = boggle_board.board[x][y]

            if len(L) == 1:
                ls = (" " + L + " ")
            else:
                ls = (" " + L)

            if cursor.x == x and cursor.y == y:
                ps += term.reverse_red(ls)
            else:
                ps += ls

            ps += vertical_line

            echo(ps + "\n")
        echo(line_row)

    # Draw the bottom row
    echo(term.move_yx((2 * (boggle_board.SIZE)), 0) + bot_row)

    # Side stuff
    column = boggle_board.SIZE * 4 + 2 + 4
    echo(term.move_yx(1, column) + "CLI Boggle Helper")
    echo(term.move_yx(2, column) + "By J. Bremen")

    echo(term.move_yx(4, column))
    echo("ESC to exit")
    echo(term.move_yx(5, column))
    echo("Arrow keys to navigate")
    echo(term.move_yx(6, column))
    echo("Press letter to place ")
    echo(term.move_yx(7, column))

    refresh_symbol = term.reverse_green("On")
    if not boggle_board.auto_refresh:
        refresh_symbol = term.reverse_red("Off")
    echo(f"TAB toggles auto refresh ({refresh_symbol})")

    echo(term.move_yx(8, column))
    echo(f"Press 1-9 to adjust size ({boggle_board.SIZE})")

    row_i = boggle_board.SIZE * 2 + 2
    row_i = max(row_i, 11)

    word_i = 0
    p = ""

    echo(term.move_yx(row_i, 0))
    echo(f"Found {len(boggle_board.last_solution)} words in {boggle_board.last_time:.2f} ms")
    row_i += 1
    echo(term.move_yx(row_i, 0))

    while word_i < len(boggle_board.last_solution):
        new = boggle_board.last_solution[word_i] + ", "
        word_i += 1

        if len(p) + len(new) < term.width:
            p += new
            continue

        if row_i > term.height - 4:
            break
        echo(p)
        p = new
        row_i += 1
        echo(term.move_yx(row_i, 0))
    print(p)

    print(f"{len(boggle_board.last_solution) - word_i} words omitted", end="", flush=True)

    return


def main():
    SIZE = 4

    term = Terminal()

    boggle_board = BoggleBoard(SIZE)

    cursor = Cursor(SIZE)

    inp = None

    loop = True

    update_flag = True

    with term.hidden_cursor(), term.cbreak(), term.fullscreen():
        while loop:
            if update_flag:
                render_entire_scene(boggle_board, cursor, term)
                update_flag = False

            inp = term.inkey(timeout=10)

            if not inp:
                continue

            if not inp.is_sequence:
                if 65 <= ord(inp.upper()) <= 90:
                    a = inp.upper()
                    print(a)
                    if a == "Q":
                        a = "Qu"

                    boggle_board.board[cursor.x][cursor.y] = a

                    if boggle_board.auto_refresh:
                        boggle_board.solve(solve_board)

                    update_flag = True

                if 49 <= ord(inp) <= 57:
                    SIZE = int(inp)
                    del boggle_board
                    del cursor
                    boggle_board = BoggleBoard(SIZE)
                    cursor = Cursor(SIZE)

                    update_flag = True

            inp_name = inp.name
            if not inp_name:
                continue

            if inp_name == "KEY_UP":
                update_flag = cursor.move_up()
            elif inp_name == "KEY_LEFT":
                update_flag = cursor.move_left()
            elif inp_name == "KEY_RIGHT":
                update_flag = cursor.move_right()
            elif inp_name == "KEY_DOWN":
                update_flag = cursor.move_down()
            elif inp_name == "KEY_ESCAPE":
                loop = False
            elif inp_name == "KEY_ENTER":
                boggle_board.solve(solve_board)
            elif inp_name in ("KEY_DELETE", "KEY_BACKSPACE"):
                boggle_board.board[cursor.x][cursor.y] = " "

                if boggle_board.auto_refresh:
                        boggle_board.solve(solve_board)

                update_flag = True

            elif inp_name == "KEY_TAB":
                boggle_board.auto_refresh = not boggle_board.auto_refresh

                if boggle_board.auto_refresh:
                    boggle_board.solve(solve_board)

                update_flag = True


if __name__ == "__main__":
    main()
