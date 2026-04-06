#pygame imports
import pygame

from game.player import Player
from game.objective import Objective


#pyside imports
from PySide6.QtWidgets import QApplication, QWidget
from menu.mainWindow import MainWindow
from menu.pauseMenu import PauseMenu

#map stuff
from maps.makeMap import load_maps, pygame_map

#other imports
import random
import subprocess
import sys

def main():
    app = QApplication.instance() or QApplication()

    window = MainWindow()
    window.setWindowTitle("Tower Defense Game")
    window.resize(400, 300)                        

    window.show()

    first = app.exec()

    if not first:

        loadedGame = window.getIsLoadedGame()
        print("Loaded Game:", loadedGame)
        
        pygame.init()
        info = pygame.display.Info()

        SCREEN_WIDTH = info.current_w
        SCREEN_HEIGHT = info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        running = True
        back_to_menu = False
        player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)
        
        # Load map once before game loop
        maps_data = load_maps()
        map_names = list(maps_data.keys())
        selected_map_name = random.choice(map_names)
        selected_map = maps_data[selected_map_name]["map"]
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = PauseMenu()
                        pause_menu.show()
                        app.exec()
                        if pause_menu.getQuit():
                            running = False
                        if pause_menu.getToMenu():
                            running = False
                            back_to_menu = True
                            

            screen.fill("black")

            # UPDATE GAME STATE
            player.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
            pygame_map(screen, SCREEN_WIDTH, selected_map, SCREEN_HEIGHT)
           
            # RENDER YOUR GAME HERE
            screen.blit(player.image, player.rect)
            
            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)  # limits FPS to 60

        pygame.quit()
        
        if back_to_menu:
            main()  # Return to main menu

if __name__ == "__main__":
    main()