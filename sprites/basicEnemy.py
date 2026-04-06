import pygame

def convert_map_coord_to_screen_coord(r: int, c: int, tile_size: int, y_offset: int) -> tuple:
    x = c * tile_size + tile_size // 2
    y = r * tile_size + y_offset + tile_size // 2
    return (x, y)

class basicEnemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, path: list, tile_size=32, y_offset=0):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

        self.path = path  
        self.path_index = 0
        self.tile_size = tile_size
        self.y_offset = y_offset
        self.speed = 2  # pixels per frame

    def update(self, tile_size: int, y_offset: int):
        self.tile_size = tile_size
        self.y_offset = y_offset
        
        if self.path and self.path_index < len(self.path):
            target_grid = self.path[self.path_index]
            target_x = target_grid[1] * tile_size + tile_size // 2 - 1
            target_y = target_grid[0] * tile_size + y_offset + tile_size // 2
            
            # Move towards target
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx**2 + dy**2)**0.5 # distance formula
            
            if distance < 5:  # Reached waypoint
                self.path_index += 1
            else:
                # Normalize and move
                self.rect.centerx += (dx / distance) * self.speed
                self.rect.centery += (dy / distance) * self.speed
    