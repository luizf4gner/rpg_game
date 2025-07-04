import pygame

class HUD:
    def __init__(self, player):
        self.font = pygame.font.SysFont("Verdana", 18, bold=True)
        self.player = player
        self.area_name = "Floresta"

        self.heart_icon = pygame.transform.scale(
            pygame.image.load("assets/icons/heart.png").convert_alpha(), (24, 24)
        )
        self.energy_icon = pygame.transform.scale(
            pygame.image.load("assets/icons/lightning.png").convert_alpha(), (24, 24)
        )

    def draw_bar(self, surface, x, y, current, max_value, color):
        ratio = current / max_value
        width = 200
        height = 20
        border_rect = pygame.Rect(x, y, width, height)
        inner_rect = pygame.Rect(x, y, width * ratio, height)

        pygame.draw.rect(surface, (0, 0, 0), border_rect, border_radius=8)
        pygame.draw.rect(surface, color, inner_rect, border_radius=8)

    def draw(self, surface):
        surface.blit(self.heart_icon, (20, 18))
        self.draw_bar(surface, 50, 20, self.player.hp, 100, (225, 0, 0))

        surface.blit(self.energy_icon, (20, 48))
        self.draw_bar(surface, 50, 50, self.player.energy, 100, (30, 144, 255))

        hp_text = self.font.render(f"{self.player.hp}/100", True, (255, 255, 255))
        en_text = self.font.render(f"{self.player.energy}/100", True, (255, 255, 255))
        area_text = self.font.render(f"Área: {self.area_name}", True, (200, 200, 255))

        surface.blit(hp_text, (260, 20))
        surface.blit(en_text, (260, 50))
        surface.blit(area_text, (600, 20))