import pygame
import os 
import json

maps_file_path = os.path.join("maps", "maps.json")

def get_len_of_rows() -> int:
    with open(maps_file_path, "r") as f:
        maps_data = json.load(f)
    return len(maps_data["grasslands"]["map"])

def get_len_of_columns() -> int:
    with open(maps_file_path, "r") as f:
        maps_data = json.load(f)
    return len(maps_data["grasslands"]["map"][0])

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, direction: pygame.math.Vector2, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255//1.5, 255//1.5, 0))
        self.rect = self.image.get_rect(center=(x, y))

        # Normalize so speed is consistent
        self.direction = direction.normalize()
        self.speed = 10

    def update(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        num_rows = get_len_of_rows()   
        num_cols = get_len_of_columns()      

        # Use same tile calculation as makeMap.py
        tile_size = SCREEN_WIDTH // num_cols
        map_height = num_rows * tile_size
        y_offset = SCREEN_HEIGHT - map_height

        # Player can move anywhere within the map bounds
        map_top = y_offset
        map_bottom = SCREEN_HEIGHT

        if self.rect.top < map_top:
            self.rect.top = map_top
            self.kill()

        if self.rect.bottom > map_bottom:
            self.rect.bottom = map_bottom
            self.kill()

        if self.rect.left < 0:
            self.rect.left = 0
            self.kill()

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.kill()
