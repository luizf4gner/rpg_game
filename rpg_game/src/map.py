import pygame

class GameMap:
    def __init__(self, map_image_path):
        raw_image = pygame.image.load(map_image_path).convert()
        self.image = pygame.transform.scale(raw_image, (800, 600))
        self.collision_rects = [
            pygame.Rect(0, 565, 800, 100),
        ]

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def check_collision(self, rect):
        return any(rect.colliderect(block) for block in self.collision_rects)

    def get_ground_y(self, rect):
        for block in self.collision_rects:
            if rect.colliderect(block):
                return block.top - rect.height
        return rect.y