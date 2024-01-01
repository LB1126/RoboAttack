import pygame
import toolbox
import math
import random
from explosion import Explosion

class WaterBalloon(pygame.sprite.Sprite):
	# Water balloon constructor function
	def __init__(self, screen, x, y, angle):
		# Makes the water balloon a sprite
		pygame.sprite.Sprite.__init__(self, self.containers)
		# Set up water balloon variables or data structure
		self.screen = screen
		self.x = x
		self.y = y
		self.angle = angle
		self.image = pygame.image.load('../assets/BalloonSmall2.png')
		self.explosion_images = []
		self.explosion_images.append(pygame.image.load('../assets/SplashSmall1.png'))
		self.explosion_images.append(pygame.image.load('../assets/SplashSmall2.png'))
		self.explosion_images.append(pygame.image.load('../assets/SplashSmall3.png'))
		self.rect = self.image.get_rect()
		self.rect.center = (self.x, self.y)
		self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
		self.speed = 10
		self.angle_rads = math.radians(self.angle)
		self.x_move = math.cos(self.angle_rads) * self.speed
		self.y_move = -math.sin(self.angle_rads) * self.speed
		self.damage = 7
		self.sfx_splash = pygame.mixer.Sound('../assets/sfx/splash.wav')

	def update(self):
		self.x += self.x_move
		self.y += self.y_move
		self.rect.center = (self.x, self.y)
		# remove the balloon if it goes to far off the screen
		if self.x < - self.image.get_width():
			self.kill()
		elif self.x > self.screen.get_width() + self.image.get_width():
			self.kill()
		elif self.y < - self.image.get_height():
			self.kill()
		elif self.y > self.screen.get_height() + self.image.get_height():
			self.kill()
		self.screen.blit(self.image, self.rect)

	def explode(self):
		self.sfx_splash.play()
		Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
		self.kill()

class WaterDroplet(WaterBalloon):
	def __init__(self, screen, x, y, angle):
		WaterBalloon.__init__(self, screen, x, y, angle)
		self.image = pygame.image.load('../assets/drop.png')
		self.rect = self.image.get_rect()
		self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
		self.damage = 3

class ExplosiveWaterBalloon(WaterBalloon):
	def __init__(self, screen, x, y, angle):
		WaterBalloon.__init__(self, screen, x, y, angle)
		self.image = pygame.image.load('../assets/Balloon.png')
		self.rect = self.image.get_rect()
		self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
		self.explosion_images = []
		self.explosion_images.append(pygame.image.load('../assets/SplashLarge1.png'))
		self.explosion_images.append(pygame.image.load('../assets/SplashLarge2.png'))
		self.explosion_images.append(pygame.image.load('../assets/SplashLarge3.png'))
		self.sfx_splash = pygame.mixer.Sound('../assets/sfx/splash-heavy.wav')

	def explode(self):
		self.sfx_splash.play()
		Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 4, False)
		self.kill()

class MagicWaterBalloon(WaterBalloon):
	def __init__(self, screen, x, y, angle):
		WaterBalloon.__init__(self, screen, x, y, angle)
		self.image = pygame.image.load('../assets/BalloonSmallMagic.png')
		self.image = pygame.image.load('../assets/BalloonSmallMagic.png')
		self.rect = self.image.get_rect()
		self.image, self.rect = toolbox.getRotatedImage(self.image, self.rect, self.angle)
		self.damage = 10
		self.speed = 50
		self.x_move = math.cos(self.angle_rads) * self.speed
		self.y_move = -math.sin(self.angle_rads) * self.speed

	def explode(self):
		MagicWaterBalloon(self.screen, self.x, self.y, random.randint(0,360))
		MagicWaterBalloon(self.screen, self.x, self.y, random.randint(0,360))
		self.sfx_splash.play()
		Explosion(self.screen, self.x, self.y, self.explosion_images, 5, 0, False)
		self.kill()

