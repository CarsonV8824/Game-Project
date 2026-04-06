#pygame imports
import pygame

from sprites.player import Player
from sprites.projectile import Projectile
from sprites.basicEnemy import basicEnemy

#pyside imports
from PySide6.QtWidgets import QApplication, QWidget
from menus.mainWindow import MainWindow
from menus.pauseMenu import PauseMenu

from sprites.fastestPath import shortest_path_networkx, convert_map_to_coords_dict
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

def convert_enemy_spawn_to_coords(map_dict: list) -> list:
    coords = []
    for r, row in enumerate(map_dict):
        for c, cell in enumerate(row):
            if cell == "enemy_spawn":
                coords.append((r, c))
    return coords

def convert_map_coord_to_screen_coord(r: int, c: int, tile_size: int, y_offset: int) -> tuple:
    x = c * tile_size + tile_size // 2 - 1
    y = r * tile_size + y_offset + tile_size // 2
    return (x, y)

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

    #sprite groups
    player_projectiles = pygame.sprite.Group()
    basicEnemys = pygame.sprite.Group()

    #Enemy spawn timers
    BASIC_ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BASIC_ENEMY_SPAWN_EVENT, 5000)

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
            if event.type == BASIC_ENEMY_SPAWN_EVENT:
                spawn_coords = convert_enemy_spawn_to_coords(selected_map)
                if spawn_coords:
                    r, c = random.choice(spawn_coords)
                    spawn_x, spawn_y = convert_map_coord_to_screen_coord(r, c, tile_size, y_offset)
                    
                    # Get path from this specific spawn location
                    enemy_path = shortest_path_networkx(selected_map_name, start_pos=(r, c))
                    
                    basic_enemy = basicEnemy(spawn_x, spawn_y, path=enemy_path, tile_size=tile_size, y_offset=y_offset)
                    basicEnemys.add(basic_enemy)

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

        collisions = pygame.sprite.groupcollide(player_projectiles, basicEnemys, True, True)
        for projectile, enemies in collisions.items():
            for enemy in enemies:
                enemy.kill()
            

        # RENDER YOUR GAME HERE
        pygame_map(screen, SCREEN_WIDTH, selected_map, SCREEN_HEIGHT)
        screen.blit(player.image, player.rect)
        player_projectiles.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
        player_projectiles.draw(screen)
        basicEnemys.update(tile_size=tile_size, y_offset=y_offset)
        basicEnemys.draw(screen)
        # flip() the display to put your work on screen
        text_surface = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(text_surface, (50, 50))

        pygame.display.flip()

        clock.tick(60)
        if clock.get_fps() <= 30:
            print("Warning: Low FPS -", clock.get_fps())

    pygame.quit()
    
    return back_to_menu