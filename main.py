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

#globals
from maps.tiles import map_colors, collision_tiles

#other imports
import random
import subprocess
import sys
import os

def main():
    stylesheet_path = os.path.join("assets", "stylesheet.css")
    with open(stylesheet_path, "r") as f:
        stylesheet = f.read()
    app = QApplication.instance() or QApplication()
    app.setStyleSheet(stylesheet)

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
        
        # Pre-calculate map constants (these don't change)
        num_cols = len(selected_map[0])
        num_rows = len(selected_map)
        tile_size = SCREEN_WIDTH // num_cols
        map_height = num_rows * tile_size
        y_offset = SCREEN_HEIGHT - map_height
        
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
            
            old_x = player.rect.centerx
            old_y = player.rect.centery
            
            player.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
            
            tile_x = player.rect.centerx // tile_size
            tile_y = (player.rect.centery - y_offset) // tile_size
            
            if 0 <= tile_x < num_cols and 0 <= tile_y < num_rows:
                current_tile = selected_map[int(tile_y)][int(tile_x)]
                if current_tile in collision_tiles():
                    player.rect.centerx = old_x
                    player.rect.centery = old_y

            # RENDER YOUR GAME HERE
            pygame_map(screen, SCREEN_WIDTH, selected_map, SCREEN_HEIGHT)
            screen.blit(player.image, player.rect)
            # flip() the display to put your work on screen
            pygame.display.flip()

            clock.tick(60)
            if clock.get_fps() <= 30:
                print("Warning: Low FPS -", clock.get_fps())

        pygame.quit()
        
        if back_to_menu:
            main()  

if __name__ == "__main__":
    main()