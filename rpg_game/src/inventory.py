import pygame
import math

class Inventory:
    def __init__(self):
        self.items = {}
        self.font = pygame.font.SysFont("Verdana", 14, bold=True)
        self.visible = False

        self.icon = pygame.transform.scale(
            pygame.image.load("assets/icons/backpack.png").convert_alpha(), (28, 28)
        )
        self.bg_color = (30, 30, 30, 220)

        self.item_icons = {
            "Poção": pygame.image.load("assets/sprites/potion2.png").convert_alpha(),
            "Espada": pygame.image.load("assets/sprites/sword.png").convert_alpha(),
        }

        self.max_slots = 20
        self.columns = 5
        self.slot_size = 64
        self.padding = 10

    def add_item(self, name):
        if name in self.items:
            self.items[name] += 1
        else:
            if len(self.items) < self.max_slots:
                self.items[name] = 1
            else:
                print("Inventário cheio!")

    def toggle(self):
        self.visible = not self.visible

    def draw(self, surface):
        if self.visible:
            inv_width = self.columns * (self.slot_size + self.padding) + self.padding
            inv_height = 4 * (self.slot_size + self.padding) + 60

            inv_surface = pygame.Surface((inv_width, inv_height), pygame.SRCALPHA)
            pygame.draw.rect(inv_surface, self.bg_color, inv_surface.get_rect(), border_radius=12)
            pygame.draw.rect(inv_surface, (180, 180, 255), inv_surface.get_rect(), 2, border_radius=12)

            inv_surface.blit(self.icon, (20, 15))
            title = self.font.render("Inventário", True, (255, 255, 255))
            inv_surface.blit(title, (60, 25))

            x_start = self.padding
            y_start = 60
            i = 0
            for name, count in self.items.items():
                row = i // self.columns
                col = i % self.columns
                x = x_start + col * (self.slot_size + self.padding)
                y = y_start + row * (self.slot_size + self.padding)

                pygame.draw.rect(inv_surface, (50, 50, 70), (x, y, self.slot_size, self.slot_size), border_radius=6)
                pygame.draw.rect(inv_surface, (120, 120, 180), (x, y, self.slot_size, self.slot_size), 2, border_radius=6)

                icon = self.item_icons.get(name)
                if icon:
                    icon_scaled = pygame.transform.scale(icon, (48, 48))
                    inv_surface.blit(icon_scaled, (x + 8, y + 8))

                count_text = self.font.render(str(count), True, (255, 255, 255))
                inv_surface.blit(count_text, (x + self.slot_size - 18, y + self.slot_size - 18))

                i += 1

            x_center = (800 - inv_width) // 2
            y_center = (600 - inv_height) // 2
            surface.blit(inv_surface, (x_center, y_center))
    
    def use_item(self, item_name, player):
        if item_name in self.items and self.items[item_name] > 0:
            self.items[item_name] -= 1
            if self.items[item_name] == 0:
                del self.items[item_name]

            if item_name == "Poção":
                player.hp = min(player.hp + 30, 100)