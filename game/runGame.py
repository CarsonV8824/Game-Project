#pygame imports
import pygame

from sprites.player import Player
from sprites.projectile import Projectile

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
import traceback

def run_game(get_loaded_game=False):
    """Run the Pygame game loop in a separate function"""
    # Initialize pygame with SDL settings
    os.environ['SDL_VIDEODRIVER'] = 'windows'
    os.environ['SDL_AUDIODRIVER'] = 'dummy'
    pygame.init()
    
    info = pygame.display.Info()

    font = pygame.font.Font(None, 36)

    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    current_wave = 1

    shoot_cooldown = 200  # milliseconds
    last_shot_time = 0

    running = True
    back_to_menu = False
    player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)

    player_projectiles = pygame.sprite.Group()

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
        try:
            events = pygame.event.get()
        except Exception as e:
            print(f"Error getting pygame events: {e}")
            traceback.print_exc()
            break
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu = PauseMenu()
                    pause_menu.show()
                    app = QApplication.instance()
                    if app:
                        app.exec()
                    if pause_menu.getQuit():
                        running = False
                    if pause_menu.getToMenu():
                        running = False
                        back_to_menu = True
                
                if event.key == pygame.K_SPACE:
                    current_time_shoot = pygame.time.get_ticks()
                    if current_time_shoot - last_shot_time >= shoot_cooldown:
                        
                        direction = pygame.math.Vector2(0, -1).rotate(player.angle)

                        projectile = Projectile(
                            x=player.rect.centerx,
                            y=player.rect.centery,
                            direction=direction,
                            SCREEN_WIDTH=SCREEN_WIDTH,
                            SCREEN_HEIGHT=SCREEN_HEIGHT
                        )
                        player_projectiles.add(projectile)
                        last_shot_time = current_time_shoot

        screen.fill("black")

        # UPDATE GAME STATE
        
        old_x = player.rect.centerx
        old_y = player.rect.centery
        
        player.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
        
        tile_x_player = player.rect.centerx // tile_size
        tile_y_player = (player.rect.centery - y_offset) // tile_size
        
        if 0 <= tile_x_player < num_cols and 0 <= tile_y_player < num_rows:
            current_tile = selected_map[int(tile_y_player)][int(tile_x_player)]
            if current_tile in collision_tiles():
                player.rect.centerx = old_x
                player.rect.centery = old_y

        tile_x_projectiles = [proj.rect.centerx // tile_size for proj in player_projectiles]
        tile_y_projectiles = [(proj.rect.centery - y_offset) // tile_size for proj in player_projectiles]
        for proj, tile_x_proj, tile_y_proj in zip(player_projectiles, tile_x_projectiles, tile_y_projectiles):
            if 0 <= tile_x_proj < num_cols and 0 <= tile_y_proj < num_rows:
                current_tile = selected_map[int(tile_y_proj)][int(tile_x_proj)]
                if current_tile in collision_tiles():
                    proj.kill()

        # RENDER YOUR GAME HERE
        pygame_map(screen, SCREEN_WIDTH, selected_map, SCREEN_HEIGHT)
        screen.blit(player.image, player.rect)
        player_projectiles.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
        player_projectiles.draw(screen)
        # flip() the display to put your work on screen
        text_surface = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(text_surface, (50, 50))

        pygame.display.flip()

        clock.tick(60)
        if clock.get_fps() <= 30:
            print("Warning: Low FPS -", clock.get_fps())

    pygame.quit()
    
    return back_to_menu