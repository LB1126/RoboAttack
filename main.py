import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from HUD import hud

# Start the game
pygame.init()
pygame.mixer.pre_init(buffer=1024)
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True
bg_image = pygame.image.load('../assets/BG_Space.png')
# Make all the Sprite groups
player_group = pygame.sprite.Group()
projectiles_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
crates_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
powerups_group = pygame.sprite.Group()

# Put every Sprite class in a group
Player.containers = player_group
WaterBalloon.containers = projectiles_group
Enemy.containers = enemies_group
Crate.containers = crates_group
Explosion.containers = explosions_group
PowerUp.containers = powerups_group

enemy_spawn_timer_max = 100
enemy_spawn_timer = 0
enemy_speedup_timer_max = 400
enemy_speedup_timer = enemy_speedup_timer_max
speed = 1

player = Player(screen, game_width/2, game_height/2)
hud = hud(screen, player)
game_started = False
def StartGame():
    global game_started
    global hud
    global player
    global enemy_spawn_timer_max
    global enemy_spawn_timer
    global enemy_speedup_timer
    enemy_spawn_timer_max = 1
    enemy_spawn_timer = 0
    enemy_speedup_timer = enemy_speedup_timer_max
    enemy_speedup_timer
    game_started = True
    hud.state = 'ingame'
    player.__init__(screen, game_width/2, game_height/2)
'''
    for i in range(0, 15):
        Crate(screen, random.randint(50,  game_width), random.randint(50, game_height), player)
        ExplosiveCrate(screen, random.randint(50,  game_width), random.randint(50, game_height), player)
'''
# ***************** Loop Land Below ***************** 
# Everything under 'while running' will be repeated over and over again
while running: 
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(bg_image, (0, 0))

    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                StartGame()
                break

    if game_started:
        keys = pygame.key.get_pressed()
        # deals with the key movement
        if keys[pygame.K_UP]:
            player.move(0, -speed, crates_group)
        if keys[pygame.K_DOWN]:
            player.move(0, speed, crates_group)
        if keys[pygame.K_RIGHT]:
            player.move(speed, 0, crates_group)
        if keys[pygame.K_LEFT]:
            player.move(-speed, 0, crates_group)
        if pygame.mouse.get_pressed()[0]:
            player.shoot()
        if keys[pygame.K_SPACE]:
            player.place_crate()
        if keys[pygame.K_e]:
            player.place_explosive_crate()

        # Gradually speed up enemy spawning
        enemy_speedup_timer -= 1
        if enemy_speedup_timer <= 0:
            if enemy_spawn_timer_max > 20:
                enemy_spawn_timer_max -= 10
            enemy_speedup_timer = enemy_speedup_timer_max

        # Make Enemy spawning happen
        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, player)
            side_to_spawn = random.randint(0, 3) # 0 = top, 1 = bottom, 2 = left, 3 = right
            if side_to_spawn == 0:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = -new_enemy.image.get_height()
            if side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = new_enemy.image.get_height() + game_height
            if side_to_spawn == 2:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
            if side_to_spawn == 3:
                new_enemy.x = new_enemy.image.get_height() + game_width
                new_enemy.y = random.randint(0, game_height)
            enemy_spawn_timer = enemy_spawn_timer_max

        for powerup in powerups_group:
            powerup.update(player)
        for explosion in explosions_group:
            explosion.update()
        for projectile in projectiles_group:
            projectile.update()
        for enemy in enemies_group:
            enemy.update(projectiles_group, crates_group, explosions_group)
        for crate in crates_group:
            crate.update(projectiles_group, explosions_group)
        player.update(enemies_group, explosions_group)
        if not player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                player_group.empty()
                enemies_group.empty()
                projectiles_group.empty()
                explosions_group.empty()
                crates_group.empty()
                powerups_group.empty()
    hud.update(player)
    # Tell pygame to update the screen       
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("ATTACK OF THE ROBOTS fps: " + str(clock.get_fps()))

