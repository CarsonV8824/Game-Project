import json
import os
import pygame
import random
from typing import Callable

from maps.tiles import map_colors, collision_tiles

maps_file_path = os.path.join("maps", "maps.json")
def load_maps() -> dict:
    with open(maps_file_path, "r") as f:
        maps_data = json.load(f)
    return maps_data

def pygame_map(screen: pygame.Surface, SCREEN_WIDTH: int, selected_map, SCREEN_HEIGHT: int=None) -> None:
    map_options = map_colors()

    tile_size = SCREEN_WIDTH // len(selected_map[0])
    map_height = len(selected_map) * tile_size
    y_offset = SCREEN_HEIGHT - map_height
    for y, row in enumerate(selected_map):
        for x, tile in enumerate(row):
            color = map_options.get(tile, (0, 0, 0))
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size + y_offset, tile_size, tile_size))