import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Gravity system
        self.vel_y = 0
        self.gravity = 0.5

    def update(self, SCREEN_WIDTH: int, SCREEN_HEIGHT: int) -> None:
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 5

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Tile height (1/11th of screen width)
        tile_h = SCREEN_WIDTH // 11

        # Map top and bottom
        map_top_y = SCREEN_HEIGHT - (tile_h * 3)
        ground_y = SCREEN_HEIGHT - tile_h

        # --- Vertical collisions ---
        # Ground collision
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0

        # Ceiling collision (top of 3‑tile map)
        if self.rect.top <= map_top_y:
            self.rect.top = map_top_y
            self.vel_y = 0

        # --- Horizontal boundaries ---
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Jumping
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.vel_y == 0:
            self.vel_y = -10