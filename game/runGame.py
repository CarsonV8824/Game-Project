#pygame imports
import pygame

from sprites.player import Player
from sprites.projectile import Projectile
from sprites.basicEnemy import basicEnemy

#pyside imports
from PySide6.QtWidgets import QApplication, QWidget
from menus.mainWindow import MainWindow
from menus.pauseMenu import PauseMenu
from menus.gameOver import GameOverScreen
from menus.upgradesMenu import UpgradesMenu

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

def run_game(get_loaded_game:bool=False) -> bool:
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

    current_wave = 4
    objective_health = 100

    shoot_cooldown = 200  # milliseconds
    last_shot_time = 0

    player = Player(x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2)
    #sprite groups
    player_projectiles = pygame.sprite.Group()
    basicEnemys = pygame.sprite.Group()

    # Wave system variables - infinite scaling
    def get_enemies_for_wave(wave):
        """Calculate enemy count for given wave (infinite scaling)"""
        return 3 + (wave - 1) * 2
    
    def get_spawn_rate_for_wave(wave):
        """Calculate spawn rate for given wave in milliseconds (infinite scaling)"""
        return max(300, 1500 - (wave - 1) * 150)
    
    enemies_spawned_this_wave = 0
    enemies_defeated_this_wave = 0
    wave_active = False
    wave_start_time = 0
    wave_downtime_end = 0  # Track when downtime ends
    WAVE_DOWNTIME = 5000  # 5 seconds in milliseconds

    #Enemy spawn timers
    BASIC_ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BASIC_ENEMY_SPAWN_EVENT, 1500)  # Start with default rate

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
    
    running = True
    back_to_menu = False
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
                    
            if event.type == BASIC_ENEMY_SPAWN_EVENT and wave_active:
                if enemies_spawned_this_wave < get_enemies_for_wave(current_wave):
                    spawn_coords = convert_enemy_spawn_to_coords(selected_map)
                    if spawn_coords:
                        r, c = random.choice(spawn_coords)
                        spawn_x, spawn_y = convert_map_coord_to_screen_coord(r, c, tile_size, y_offset)
                        
                        # Get path from this specific spawn location
                        enemy_path = shortest_path_networkx(selected_map_name, start_pos=(r, c))
                        
                        basic_enemy = basicEnemy(spawn_x, spawn_y, path=enemy_path, tile_size=tile_size, y_offset=y_offset)
                        basicEnemys.add(basic_enemy)
                        enemies_spawned_this_wave += 1

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

        tile_x_enemies = [enemy.rect.centerx // tile_size for enemy in basicEnemys]
        tile_y_enemies = [(enemy.rect.centery - y_offset) // tile_size for enemy in basicEnemys]
        for enemy, tile_x_enemy, tile_y_enemy in zip(basicEnemys, tile_x_enemies, tile_y_enemies):
            if 0 <= tile_x_enemy < num_cols and 0 <= tile_y_enemy < num_rows:
                current_tile = selected_map[int(tile_y_enemy)][int(tile_x_enemy)]
                if current_tile == "objective":
                    enemy.kill()
                    objective_health -= 10
                    enemies_defeated_this_wave += 1

        collisions = pygame.sprite.groupcollide(player_projectiles, basicEnemys, True, True)
        for projectile, enemies in collisions.items():
            for enemy in enemies:
                enemy.kill()
                projectile.kill()
                enemies_defeated_this_wave += 1

        if objective_health <= 0:
            game_over_screen = GameOverScreen(score=current_wave)
            game_over_screen.show()
            game_over_app = QApplication.instance()
            if game_over_app:
                game_over_app.exec()
            if game_over_screen.getIsMainMenu():
                back_to_menu = True
                running = False
            running = False
        
        # Check if wave is complete
        if wave_active and enemies_spawned_this_wave > 0:
            if enemies_spawned_this_wave == enemies_defeated_this_wave and len(basicEnemys) == 0:
                # All enemies defeated, start downtime
                wave_active = False
                wave_downtime_end = pygame.time.get_ticks() + WAVE_DOWNTIME
                
                # Prepare next wave
                current_wave += 1
                enemies_spawned_this_wave = 0
                enemies_defeated_this_wave = 0
                
                # Update spawn rate for new wave
                spawn_rate = get_spawn_rate_for_wave(current_wave)
                pygame.time.set_timer(BASIC_ENEMY_SPAWN_EVENT, spawn_rate)
                
                # Change map every 5 waves
                if current_wave % 5 == 0:
                    selected_map_name = random.choice(map_names)
                    selected_map = maps_data[selected_map_name]["map"]
                    upgrades_menu = UpgradesMenu()
                    upgrades_menu.show()
                    upgrades_app = QApplication.instance()
                    if upgrades_app:
                        upgrades_app.exec()
        
        # Auto-start next wave after downtime
        current_time = pygame.time.get_ticks()
        if not wave_active and wave_downtime_end > 0 and current_time >= wave_downtime_end:
            wave_active = True
            wave_downtime_end = 0
        
        # Start wave automatically (works for any wave, not just wave 1)
        if not wave_active and wave_downtime_end == 0:
            wave_active = True

        pygame_map(screen, SCREEN_WIDTH, selected_map, SCREEN_HEIGHT)
        screen.blit(player.image, player.rect)
        player_projectiles.update(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
        player_projectiles.draw(screen)
        basicEnemys.update(tile_size=tile_size, y_offset=y_offset)
        basicEnemys.draw(screen)
        
        #all text
        text_surface = font.render(f"FPS: {clock.get_fps():.1f}", True, (255, 255, 255))
        screen.blit(text_surface, (50, 50))

        wave_text = font.render(f"Wave: {current_wave}", True, (255, 255, 255))
        screen.blit(wave_text, (50, 100))

        objective_health_text = font.render(f"Objective Health: {objective_health}", True, (255, 255, 255))
        screen.blit(objective_health_text, (50, 150))
        
        # Wave status display
        if wave_active:
            enemies_left = enemies_spawned_this_wave - enemies_defeated_this_wave
            total_enemies = get_enemies_for_wave(current_wave)
            status_text = font.render(f"Enemies: {enemies_left}/{total_enemies}", True, (255, 255, 0))
            screen.blit(status_text, (50, 200))
        elif wave_downtime_end > 0:
            # Show countdown during downtime
            time_left = max(0, (wave_downtime_end - pygame.time.get_ticks()) / 1000)
            status_text = font.render(f"Next wave in: {time_left:.1f}s", True, (255, 255, 0))
            screen.blit(status_text, (50, 200))
        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    
    return back_to_menu