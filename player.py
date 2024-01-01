import pygame
import toolbox
import projectile 
from crate import Crate
from crate import ExplosiveCrate
class Player(pygame.sprite.Sprite):
    # Player constructor function (stuff that happens right when you make the player)
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.screen = screen
        self.x = x
        self.y = y
        self.image = pygame.image.load('../assets/Player_02.png')
        self.image_hurt = pygame.image.load('../assets/Player_02hurted.png')
        self.image_defeated =  pygame.image.load('../assets/Enemy_01.png')
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.speed = 8
        self.angle = 0
        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 7.5
        self.health_max = 100 
        self.health = self.health_max
        self.health_bar_width = self.image.get_width()
        self.health_bar_height = 8
        self.health_bar_green = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.health_bar_red = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)
        self.alive = True
        self.hurt_timer = 0
        self.crate_ammo = 10
        self.crate_cooldown = 0
        self.crate_cooldown_max = 10
        self.explosive_crate_ammo = 10
        self.explosive_crate_cooldown = 0
        self.explosive_crate_cooldown_max = 10
        self.lives = 3
        self.shot_type = 'normal'
        self.special_ammo = 0
        self.score = 0
        self.sfx_shot = pygame.mixer.Sound('../assets/sfx/shot.wav')
        self.sfx_place = pygame.mixer.Sound('../assets/sfx/bump.wav')
        self.sfx_defeat = pygame.mixer.Sound('../assets/sfx/electrocute.wav')
        self.speed_timer = 0


# Player update function (stuff to happen over and over agian)
    def update(self, enemies, explosions):
        # Check for collisison with Enemies
        self.rect.center = (self.x, self.y)
        self.speed_timer -= 1
        if self.speed_timer <=0:
            self.speed = 8
        for explosion in explosions:
            if explosion.damage and explosion.damage_player:
                if self.rect.colliderect(explosion.rect):
                    self.getHit(explosion.damage)
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.getHit(0)
                self.getHit(enemy.damage)
        keys = pygame.key.get_pressed()
        if self.alive:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.angle = toolbox.angleBetweenPoints(self.x, self.y, mouse_x, mouse_y)

        self.rect.center = (self.x, self.y)
        if self.alive:
            if self.hurt_timer > 0:
                image_to_rotate = self.image_hurt
                self.hurt_timer -= 1
            else:
                image_to_rotate = self.image
        else:
            image_to_rotate = self.image_defeated
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.crate_cooldown > 0:
            self.crate_cooldown -= 1
        if self.explosive_crate_cooldown > 0:
            self.explosive_crate_cooldown -= 1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
        self.x = self.rect.centerx
        self.y = self.rect.centery
        # Get the rotated version of the player picture
        image_to_draw, image_rect = toolbox.getRotatedImage(image_to_rotate, self.rect, self.angle)
        self.screen.blit(image_to_draw, image_rect)

        # Move and draw the health bar
        self.health_bar_red.x = self.rect.x
        self.health_bar_red.bottom = self.rect.y - 5
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_bar_red)
        self.health_bar_green.topleft = self.health_bar_red.topleft
        health_percentage = self.health / self.health_max
        self.health_bar_green.width = self.health_bar_width * health_percentage
        if self.alive:
            pygame.draw.rect(self.screen, (0, 255, 0), self.health_bar_green)

# Move function (makes the player move)
    def move(self, x_movement, y_movement, crates):
        if self.alive:
            # Move test_rect first to make sure the player doesn't overlap a crate
            test_rect = self.rect
            test_rect.x += self.speed * x_movement
            test_rect.y += self.speed * y_movement
            collision = False
            for crate in crates:
                if not crate.just_placed:
                    if test_rect.colliderect(crate.rect):
                        collision = True
            if not collision:
                self.x += self.speed * x_movement
                self.y += self.speed * y_movement

# Shoot function (maker a new balloon)
    def shoot(self):
        if self.shoot_cooldown <= 0 and self.alive:
            self.sfx_shot.play()
            if self.shot_type == 'normal':
                self.speed = 8
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
            elif self.shot_type == 'split':
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle - 15)
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle)
                projectile.WaterBalloon(self.screen, self.x, self.y, self.angle + 15)
                self.speed = 8
                self.special_ammo -= 1
            elif self.shot_type == 'stream':
                projectile.WaterDroplet(self.screen, self.x, self.y, self.angle)
                self.speed = 8
                self.special_ammo -= 1
            elif self.shot_type == 'burst':
                projectile.ExplosiveWaterBalloon(self.screen, self.x, self.y, self.angle)
                self.speed = 8
                self.special_ammo -= 1
            elif self.shot_type == 'magic':
                projectile.MagicWaterBalloon(self.screen, self.x, self.y, self.angle)
                self.special_ammo = 999
                self.shoot_cooldown_max = 3
            self.shoot_cooldown = self.shoot_cooldown_max
            if self.special_ammo <= 0:
                self.power_up('normal')


    # Get hit function(makes the player take damage)
    def getHit(self, damage):
        if self.alive:
            self.hurt_timer = 5
            self.health -= damage
            if self.health <= 0:
                self.health = 100
                self.lives -= 1
                if self.lives <= 0:
                    self.sfx_defeat.play() 
                    self.alive = False

    def place_crate(self):
        if self.alive and self.crate_ammo > 0 and self.crate_cooldown <= 0:
            self.sfx_place.play()
            Crate(self.screen, self.x+5, self.y-5, self)
            self.crate_ammo -= 1
            self.crate_cooldown = self.crate_cooldown_max

    def place_explosive_crate(self):
        if self.alive and self.explosive_crate_ammo > 0 and self.explosive_crate_cooldown <= 0:
            self.sfx_place.play()
            ExplosiveCrate(self.screen, self.x+5, self.y-5, self)
            self.explosive_crate_ammo -= 1
            self.explosive_crate_cooldown = self.explosive_crate_cooldown_max

    # how to pick up power ups 
    def power_up(self, power_type):
        if power_type == 'crateammo':
           self.crate_ammo += 10
           self.get_score(10)
        elif power_type == 'explosiveammo':
           self.explosive_crate_ammo += 10
           self.get_score(10)
        elif power_type == 'split':
            self.shot_type = 'split'
            self.special_ammo = 40
            self.shoot_cooldown_max = 15
            self.get_score(20)
        elif power_type == 'normal':
            self.shot_type = 'normal'
            self.shoot_cooldown_max = 7.5
        elif power_type == 'stream':
            self.shot_type = 'stream'
            self.special_ammo = 300
            self.shoot_cooldown_max = 3
            self.get_score(20)
        elif power_type == 'burst':
            self.shot_type = 'burst'
            self.special_ammo = 45
            self.shoot_cooldown_max = 22.5
            self.get_score(20)
        elif power_type == 'health':
            if self.health <= 65:
                self.health += 35
            elif self.health > 65:
                self.health = 100
            self.get_score(10)
        elif power_type == 'magic':
            self.shot_type = 'magic'
            self.speed = 12
            self.shoot_cooldown_max = 3
            self.health += 10
            self.speed_timer = 400
            self.get_score(20)

    def get_score(self, score):
        if self.alive:
            self.score += score
