# CLI-Boggle
Python 3 program to solve a boggle board input within the command line interface. CLI using the Blessed Library. Developed using a backtracking Boggle solving algorithm that I wrote a few years ago, using a Trie datastructure for fast word verification. It should work accross Mac, Linux, and PC platforms.

![CLI Boggle Game Demo](https://user-images.githubusercontent.com/15671813/124226764-3c51a080-dacf-11eb-8fa0-b9b8138f649d.gif)


## Program Setup
1. Install the needed libraries(s). The only library not installed in the default Python installation is blessed, which may be installed via `pip install blessed`
2. Navigate to the directory in your preferred terminal

## Program Use
1. Run the program with `python cli_boggle.py`, or however you choose to run your python files
2. Select your board size by pressing the number that corresponds to the width and height of the board
3. Using the arrow keys, move the cursor (denoted by the highlighted square). 
4. Press the letter key when in the desired square to fill in the board
5. All possible words will be displayed below the board live; this can be toggled by pressing `TAB` if performance gets to be an issue. 
  - Is not an issue on most systems
6. You can press the number keys to clear the board when you're ready to enter the next one, or write over letters by pressing a different key
7. Press `ESC` to exit out of the program. The screen will be returned to its state before the application was launched


## Program Details
- CLI Boggle uses recursive backtracking to go through all possible words, using a Trie datastructure to detect if a word has been found. It also backtracks when it gets to a point such that no more words can be made. 
- I wrote this algorithm in 2018 [Original Repository](https://github.com/readjfb/boggle_player)
- The [Blessed](https://github.com/jquast/blessed) library for Python 3 is used to create the command line interface


## Contributing
Pull requests and reccomendations for changes are welcome. For major changes, please open an issue first to discuss what you would like to change, to avoid having multiple solutions to an issue.

## License 
[MIT License](LICENSE)


