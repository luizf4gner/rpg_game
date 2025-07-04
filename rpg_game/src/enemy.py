import pygame
import random

class Enemy:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = 50
        self.speed = 1
        self.direction = random.choice(["left", "right"])
        self.move_timer = 0

        self.vel_y = 0
        self.gravity = 0.5
        self.on_ground = False

    def update(self, player_rect, game_map):
        self.move_timer += 1
        if self.move_timer > 60:
            self.direction = random.choice(["left", "right"])
            self.move_timer = 0

        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        self.vel_y += self.gravity
        dy = self.vel_y

        new_rect = self.rect.move(0, dy)

        if not game_map.check_collision(new_rect):
            self.rect = new_rect
            self.on_ground = False
        else:
            if self.vel_y > 0:
                self.on_ground = True
                self.vel_y = 0
                self.rect.y = game_map.get_ground_y(self.rect)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)

        return self.rect.colliderect(player_rect)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def take_damage(self, amount):
        self.hp -= amount
        return self.hp <= 0