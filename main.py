from game.runGame import run_game
from sprites.menus import show_menu
import sys

from sprites.fastestPath import shortest_path_networkx

def main():
    """Main entry point"""
    loadedGame = show_menu()
     
    if loadedGame is not None:
        back_to_menu = run_game(loadedGame)
        if back_to_menu:
            main()
    else:
        sys.exit()

if __name__ == "__main__":
    main()