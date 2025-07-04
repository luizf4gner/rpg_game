import pygame

class Item:
    def __init__(self, x, y, image_path, name):
        original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        self.collected = False
        
    def draw(self, surface):
        if not self.collected:
            surface.blit(self.image, self.rect.topleft)
            
    def check_pickup(self, player_rect, keys):
        if not self.collected and self.rect.colliderect(player_rect):
            if keys[pygame.K_e]:
                self.collected = True
                return self.name
        return None