import pygame
import os

def load_image(path, size=(94, 94)):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

class Player:
    def __init__(self, x, y):
        self.facing_right = True
        self.animations = {
            "idle": [load_image("assets/sprites/player/walk1.png")],
            "walk": [
                load_image(f"assets/sprites/player/walk{i}.png")
                for i in range(1, 5)
            ]
        }

        self.state = "idle"
        self.frame_index = 0
        self.frame_timer = 0
        self.animation_speed = 20

        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3

        self.hp = 100
        self.energy = 100

        self.vel_y = 0
        self.jump_strength = -10
        self.gravity = 0.5
        self.on_ground = False

        self.attacking = False
        self.attack_cooldown = 0

        self.weapon_image = load_image("assets/sprites/sword.png", size=(64, 64))
        self.weapon_offset = (0, 10)

    def update(self, keys, game_map):
        dx = 0
        moving = False

        if keys[pygame.K_a]:
            dx = -self.speed
            moving = True
        if keys[pygame.K_d]:
            dx = self.speed
            moving = True

        if dx > 0:
            self.facing_right = False
        elif dx < 0:
            self.facing_right = True

        self.state = "walk" if moving else "idle"
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0

        self.vel_y += self.gravity
        dy = self.vel_y

        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        new_rect = self.rect.move(dx, dy)
        if not game_map.check_collision(new_rect):
            self.rect = new_rect
            self.on_ground = False
        else:
            if self.vel_y > 0:
                self.on_ground = True
                self.vel_y = 0
                self.rect.y = game_map.get_ground_y(self.rect)
            elif self.vel_y < 0:
                self.vel_y = 0

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if keys[pygame.K_SPACE] and self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 20
        else:
            self.attacking = False

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(800, self.rect.right)

        self.frame_index += 1
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.state])
            
        if self.frame_index >= len(self.animations[self.state]):
            self.frame_index = 0
            
        self.image = self.animations[self.state][self.frame_index]

    def draw(self, surface, active_item=None):
        image = pygame.transform.flip(self.image, not self.facing_right, False)
        surface.blit(image, self.rect.topleft)
        if active_item == "Espada":
            pos = (self.rect.x + self.weapon_offset[0], self.rect.y + self.weapon_offset[1])
            surface.blit(self.weapon_image, pos)