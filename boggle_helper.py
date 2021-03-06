"""
Made by Jackson Bremen
Written Summer 2018, Refactored Winter 2020, refactored Summer 2021
Trie Datastructure used from vivekn (github below)
Considerable additional functionality added
"""


class Trie:
    # https://github.com/vivekn/autocomplete/blob/master/trie.py#L11
    def __init__(self):
        self.children = {}
        self.flag = False  # Flag to represent that a word ends at this node

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.flag = True

    def contains(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.flag

    def one_autocomplete(self, prefix):
        node = self
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


dictionary = Trie()
with open("allScrabbleWords.txt", "r") as file:
    for i in file.read().split():
        dictionary.insert(i)


def adjacent(val1, val2, lst):
    try:
        return lst.index(val1) - lst.index(val2) in [-1, 1]
    except ValueError:
        return False
    return False


def solve_board(board):
    def turtle(board, x, y, inv_spaces, letters=""):
        # Make a copy of the input, so that we're not modifying the orignals
        inv_spaces = [*inv_spaces]

        # crossing lets the path cross over itself diagonaly [if true];
        # min_num_lett is the min number of letters for a word
        crossing, min_num_lett = True, 3

        inv_spaces.append((x, y))
        letters += str(board[x][y])

        # checking to see if the current path has made a letter, and if it has
        # been the right length
        if dictionary.contains(letters) and len(letters) >= min_num_lett:
            all_words.add(letters)

        # if there are no more possible words
        elif not dictionary.one_autocomplete(letters):
            return 0

        # p0 p1 p2
        # p3 X  p4
        # p5 p6 p7

        p0 = (x - 1, y - 1)
        p1 = (x, y - 1)
        p2 = (x + 1, y - 1)
        p3 = (x - 1, y)
        p4 = (x + 1, y)
        p5 = (x - 1, y + 1)
        p6 = (x, y + 1)
        p7 = (x + 1, y + 1)

        if p4 not in inv_spaces:
            turtle(board, *p4, inv_spaces, letters)

        if p3 not in inv_spaces:
            turtle(board, *p3, inv_spaces, letters)

        if p1 not in inv_spaces:
            turtle(board, *p1, inv_spaces, letters)

        if p6 not in inv_spaces:
            turtle(board, *p6, inv_spaces, letters)

        if not crossing:
            if p0 not in inv_spaces and not adjacent(p3, p1, inv_spaces):
                turtle(board, *p0, inv_spaces, letters)

            if p2 not in inv_spaces and not adjacent(p4, p1, inv_spaces):
                turtle(board, *p2, inv_spaces, letters)

            if p5 not in inv_spaces and not adjacent(p3, p6, inv_spaces):
                turtle(board, *p5, inv_spaces, letters)

            if p7 not in inv_spaces and not adjacent(p4, p6, inv_spaces):
                turtle(board, *p7, inv_spaces, letters)

        else:
            # diagonals, allows crossing over
            if p0 not in inv_spaces:
                turtle(board, *p0, inv_spaces, letters)

            if p2 not in inv_spaces:
                turtle(board, *p2, inv_spaces, letters)

            if p5 not in inv_spaces:
                turtle(board, *p5, inv_spaces, letters)

            if p7 not in inv_spaces:
                turtle(board, *p7, inv_spaces, letters)

    # all_words is global, as lists are global by default in python
    all_words = set([])
    # board exterior is a list of the points on the exterior of the board, such
    # that the turtle won't go to them
    board_exterior = [(-1, -1)]
    for i in range(len(board) + 1):
        board_exterior.append((-1, i))
        board_exterior.append((len(board), i))
        board_exterior.append((i, -1))
        board_exterior.append((i, len(board)))

    for x, y_l in enumerate(board):
        for y, x_l in enumerate(y_l):
            turtle(board, x, y, [*board_exterior])

    return all_words


def score_calc(words):
    val_table = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 5, 8: 11}
    total = 0
    num_chars = 0
    for item in words:
        if len(item) not in val_table:
            total += 11
        else:
            total += val_table[len(item)]
        num_chars += len(item)
    return total, num_chars


if __name__ == "__main__":
    board = [["D", "O"], ["G", "S"]]

    solution = solve_board(board)
    print(len(solution), len(set(solution)))
    print(
        ",".join(solution),
        "\n",
        len(solution),
        "words, max score is:",
        str(score_calc(solution)),
        "characters",
    )
