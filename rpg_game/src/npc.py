import pygame

class NPC:
    def __init__(self, x, y, image_path, name, dialogue_lines):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.name = name
        self.dialogue_lines = dialogue_lines
        self.current_line = 0
        self.font = pygame.font.SysFont("Arial", 18)
        self.talking = False
        self.awaiting_choice = False
        self.challenge_accepted = False

    def update(self, player_rect, keys):
        if self.rect.colliderect(player_rect):
            if keys[pygame.K_e]:
                self.talking = True
        else:
            self.talking = False
            self.current_line = 0
            self.awaiting_choice = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def draw_dialogue(self, surface):
        if self.talking:
            pygame.draw.rect(surface, (0, 0, 0), (50, 500, 700, 80))
            pygame.draw.rect(surface, (225, 225, 225), (50, 500, 700, 80), 2)

            if self.awaiting_choice:
                text = f"{self.name}: Aceita o desafio? (Enter = Sim, Esc = Não)"
            else:
                text = f"{self.name}: {self.dialogue_lines[self.current_line]}"
            rendered = self.font.render(text, True, (225, 225, 225))
            surface.blit(rendered, (60, 530))

    def advance_dialogue(self):
        if self.talking and not self.awaiting_choice:
            self.current_line += 1
            if self.current_line >= len(self.dialogue_lines):
                self.awaiting_choice = True
                self.current_line = len(self.dialogue_lines) - 1

    def handle_choice(self, event):
        if self.awaiting_choice:
            if event.key == pygame.K_RETURN:
                self.challenge_accepted = True
                self.talking = False
                self.awaiting_choice = False
            elif event.key == pygame.K_ESCAPE:
                self.talking = False
                self.awaiting_choice = False