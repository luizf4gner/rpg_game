import pygame

class Hotbar:
    def __init__(self, inventory):
        self.inventory = inventory
        self.slots = [None] * 5
        self.selected = 0
        self.font = pygame.font.SysFont("Arial", 14)

    def assign_from_inventory(self):
        keys = list(self.inventory.items.keys())
        for i in range(len(self.slots)):
            if i < len(keys):
                self.slots[i] = keys[i]
            else:
                self.slots[i] = None

    def handle_input(self, event):
        if pygame.K_1 <= event.key <= pygame.K_5:
            self.selected = event.key - pygame.K_1

    def draw(self, surface):
        x = 250
        y = 552
        slot_size = 36
        padding = 6

        for i in range(5):
            rect = pygame.Rect(x + i * (slot_size + padding), y, slot_size, slot_size)
            color = (180, 180, 220) if i == self.selected else (80, 80, 80)
            pygame.draw.rect(surface, color, rect, border_radius=4)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1, border_radius=4)

            item_name = self.slots[i]
            if item_name and item_name in self.inventory.item_icons:
                icon = pygame.transform.scale(self.inventory.item_icons[item_name], (24, 24))
                surface.blit(icon, (rect.x + 6, rect.y + 6))

            num_text = self.font.render(str(i + 1), True, (255, 255, 255))
            surface.blit(num_text, (rect.x + 2, rect.y + 2))

    def get_active_item(self):
        return self.slots[self.selected]