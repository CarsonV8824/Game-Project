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

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        
        self.base_image = pygame.Surface((50, 50))
        self.base_image.fill((50, 50, 50))  
        
        pygame.draw.polygon(self.base_image, (255, 0, 0), [(25, 5), (35, 40), (15, 40)])
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.resources = {"wood": 0, "stone": 0, "water": 0}
        self.angle = 0
        self.rotation_speed = 2
        self.movement_speed = 5
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)

    def update(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.rotation_speed
        
        
        self.direction = pygame.math.Vector2(0, -1).rotate(self.angle)
        
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.x += self.direction.x * self.movement_speed
            self.rect.y += self.direction.y * self.movement_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.x -= self.direction.x * self.movement_speed
            self.rect.y -= self.direction.y * self.movement_speed

        
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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

        if self.rect.bottom > map_bottom:
            self.rect.bottom = map_bottom

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH