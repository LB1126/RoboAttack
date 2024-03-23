import pygame

class Explosion(pygame.sprite.Sprite):
	def __init__(self, screen, x, y, images, duration, damage, damage_player):
		# Make explosion inherit Sprite
		pygame.sprite.Sprite.__init__(self, self.contaibners)
		# Set up explosion variables
		self.screen = screen
		self.x = x
		self.y = y
		self.images = images
		self.duration = duration
		self.damage = damage
		self.rect = self.images[0].get_rect()
		self.rect.center = (self.x, self.y)
		self.animation_timer = duration
		self.frame_to_draw = 0
		self.last_frame = len(self.images) - 1
		self.damage_player = damage_player

	def update(self):
		self.animation_timer -= 1
		if self.animation_timer <= 0:
			if self.frame_to_draw < self.last_frame:
				self.frame_to_draw += 1
				self.animation_timer = self.duration
			else:
				self.kill()
		self.screen.blit(self.images[self.frame_to_draw], self.rect)