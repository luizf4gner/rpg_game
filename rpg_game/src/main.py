import pygame
from player import Player
from map import GameMap
from hud import HUD
from npc import NPC
from item import Item
from inventory import Inventory
from enemy import Enemy
from hotbar import Hotbar
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

inventory = Inventory()
hotbar = Hotbar(inventory)
player = Player(100, 100)
game_map = GameMap("assets/tiles/map4.png")
npc = NPC(100, 465, "assets/sprites/anciao.png", "Ancião", [
    "Olá, Jovem aventureiro...",
    "Uma criatura se esconde nas sombras da floresta.",
    "Derrote-a e conseguirá uma grande recompensa!"
])
item1 = Item(400, 545, "assets/sprites/potion.png", "Poção")
sword_item = Item(600, 545, "assets/sprites/sword.png", "Espada")
sword_spawned = False
items = [item1]
enemies = []
hud = HUD(player)
enemy_spawned = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inventory.toggle()
            elif event.key == pygame.K_v:
                inventory.use_item("Poção", player)
                hotbar.assign_from_inventory()
            elif event.key == pygame.K_e:
                npc.advance_dialogue()
            else:
                npc.handle_choice(event)
                hotbar.handle_input(event)

    keys = pygame.key.get_pressed()
    player.update(keys, game_map)
    npc.update(player.rect, keys)

    if npc.challenge_accepted and not enemy_spawned:
        enemy1 = Enemy(500, 300, "assets/sprites/enemy2.png")
        enemies.append(enemy1)
        enemy_spawned = True
    
    game_map.draw(screen)

    for enemy in enemies[:]:
        if enemy.update(player.rect, game_map):
            player.hp -= 0.5
        if player.attacking and player.rect.colliderect(enemy.rect):
            activate_item = hotbar.get_active_item()
            damage = 25 if not activate_item == "Espada" else 10
            
            if enemy.take_damage(damage):
                enemies.remove(enemy)
                if not sword_spawned:
                    items.append(sword_item)
                    sword_spawned = True
    
    for enemy in enemies:
        enemy.draw(screen)

    for item in items:
        name = item.check_pickup(player.rect, keys)
        if name:
            inventory.add_item(name)
            hotbar.assign_from_inventory()

    player.draw(screen, active_item=hotbar.get_active_item())
    npc.draw(screen)

    for item in items:
        item.draw(screen)

    npc.draw_dialogue(screen)
    hud.draw(screen)
    inventory.draw(screen)
    hotbar.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    
    if player.hp <= 0:
        screen.fill((0,0,0))
        font = pygame.font.SysFont("Arial", 36, bold=True)
        text = font.render("Você morreu!", True, (255, 0, 0))
        screen.blit(text, (300, 280))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

pygame.quit()
sys.exit()