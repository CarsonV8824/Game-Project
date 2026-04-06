import json
import os
import pygame
import random
from typing import Callable

maps_file_path = os.path.join("maps", "maps.json")
def load_maps() -> dict:
    with open(maps_file_path, "r") as f:
        maps_data = json.load(f)
    return maps_data

def pygame_map(screen: pygame.Surface, SCREEN_WIDTH: int, selected_map, SCREEN_HEIGHT: int=None) -> None:
    map_options = {
        "air": (135, 206, 235),
        "leaves": (34, 139, 34),
        "log": (139, 69, 19),
        "green_land": (0, 255, 0),
        "cactus": (0, 100, 0),
        "sand": (194, 178, 128),
        "ice_block": (173, 216, 230),
        "snow": (255, 250, 250)
    }

    tile_size = SCREEN_WIDTH // len(selected_map[0])  # Assuming all rows have the same number of tiles
    map_height = len(selected_map) * tile_size
    y_offset = SCREEN_HEIGHT - map_height
    for y, row in enumerate(selected_map):
        for x, tile in enumerate(row):
            color = map_options.get(tile, (0, 0, 0))
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size + y_offset, tile_size, tile_size))

    