import pygame
import random
import toolbox


class PowerUp(pygame.sprite.Sprite):
	def __init__(self, screen, x, y):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.screen = screen
		self.x = x
		self.y = y
		self.pick_power = random.randint(6, 6)
		if self.pick_power == 0: # crate ammo
			self.image = pygame.image.load('../assets/powerupCrate.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundBlue.png')
			self.power_type = 'crateammo'
		elif self.pick_power == 1: # explosive ammo
			self.image = pygame.image.load('../assets/powerupExplosiveBarrel.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundBlue.png')
			self.power_type = 'explosiveammo'
		elif self.pick_power == 2: # split shot
			self.image = pygame.image.load('../assets/powerupSplit.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundRed.png')
			self.power_type = 'split'
		elif self.pick_power == 5: # stream
			self.image = pygame.image.load('../assets/powerupDrop.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundRed.png')
			self.power_type = 'stream'
		elif self.pick_power == 4: # burst
			self.image = pygame.image.load('../assets/SplashSmall1.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundRed.png')
			self.power_type = 'burst'
		elif self.pick_power == 3: # health
			self.image = pygame.image.load('../assets/heart.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundBlue.png')
			self.power_type = 'health'
		elif self.pick_power == 6: # health
			self.image = pygame.image.load('../assets/BalloonSmallMagic.png')
			self.background_image = pygame.image.load('../assets/powerupBackgroundRed.png')
			self.power_type = 'magic'
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.background_angle = 0
		self.spin_speed = 2
		self.despawn_timer = 400
		self.sfx_pickup = pygame.mixer.Sound('../assets/sfx/powerup.wav')

	def update(self, player): 
		if self.rect.colliderect(player.rect):
			self.sfx_pickup.play()
			player.power_up(self.power_type)
			self.kill()
		self.despawn_timer -= 1
		if self.despawn_timer <= 0:
			self.kill()
		self.background_angle += self.spin_speed
		bg_image_to_draw, bg_rect = toolbox.getRotatedImage(self.background_image, self.rect, self.background_angle)
		if self.despawn_timer > 100:
			self.screen.blit(bg_image_to_draw, bg_rect)
			self.screen.blit(self.image, self.rect)
		elif self.despawn_timer < 100 and self.despawn_timer % 10 > 5: 
			self.screen.blit(bg_image_to_draw, bg_rect)
			self.screen.blit(self.image, self.rect)
				