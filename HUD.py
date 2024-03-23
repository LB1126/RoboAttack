import pygame
import toolbox
from player import Player

class hud():
	def __init__(self, screen, player):
		self.screen = screen
		self.player = player
		self.state = 'mainmenu'
		self.hud_font = pygame.font.SysFont('skia', 30)
		self.hud_font_med = pygame.font.SysFont("skia", 50)
		self.hud_font_big = pygame.font.SysFont('skia', 80)
		self.live_font = pygame.font.SysFont('skia', 30)
		self.health_font = pygame.font.SysFont('skia', 30)
		# Load stuff for the main menu
		self.title_image = pygame.image.load('../assets/title.png')
		self.start_text = self.hud_font.render('Press any key to start', True, (0,0,0))
		self.tutorial_text = self.hud_font.render("URDL to move - CLICK to shoot - SPACE for a crate - E for explosive crate", True, (0, 0, 0))
		#Load stuff for the game over screen
		self.game_over_text = self.hud_font_big.render('Game Over', True, (255, 0, 0))
		self.reset_button = pygame.image.load('../assets/BtnReset.png')
		# Crate Ammo tiles
		self.crate_icon = pygame.image.load('../assets/Crate.png')
		self.explosive_crate_icon = pygame.image.load('../assets/ExplosiveBarrel.png')
		self.crate_ammo_tile = AmmoTile(self.screen, self.crate_icon, self.hud_font)
		self.explosive_crate_ammo_tile = AmmoTile(self.screen, self.explosive_crate_icon, self.hud_font)
		# Speacial Water Balloon/ Water Ammo Tiles
		self.split_shot_icon = pygame.image.load('../assets/iconSplit.png')
		self.burst_shot_icon = pygame.image.load('../assets/SplashSmall1.png')
		self.stream_shot_icon = pygame.image.load('../assets/iconStream.png')
		self.normal_shot_icon = pygame.image.load('../assets/BalloonSmall2.png')
		self.magic_shot_icon = pygame.image.load('../assets/BalloonSmallMagic.png')
		self.balloon_ammo_tile = AmmoTile(self.screen, self.normal_shot_icon, self.hud_font)	

	def update(self, player):
		if self.state == 'ingame':
			tile_x = 400
			self.score_text = self.hud_font.render("score:" + str(self.player.score), True, (255, 255, 255))
			self.live_text = self.live_font.render("Lives Left: "+ str(player.lives), 1, (255, 255, 255))
			self.health_text = self.health_font.render('Health: ' + str(player.health), 1, (255, 255, 255))
			self.screen.blit(self.score_text, (10, 10))
			self.screen.blit(self.live_text, (830, 10))
			self.screen.blit(self.health_text, (415, 10))
			self.crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.crate_ammo)
			tile_x += self.crate_ammo_tile.width
			self.explosive_crate_ammo_tile.update(tile_x, self.screen.get_height(), self.player.explosive_crate_ammo)
			tile_x += self.explosive_crate_ammo_tile.width
			# figure put which icon to use for speacial ammo
			if self.player.shot_type == 'normal':
				self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), 0)
				self.balloon_ammo_tile.icon = self.normal_shot_icon
			elif self.player.shot_type == 'split':
				self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.split_ammo)
				self.balloon_ammo_tile.icon = self.split_shot_icon
			elif self.player.shot_type == 'stream':
				self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.stream_ammo)
				self.balloon_ammo_tile.icon = self.stream_shot_icon
			elif self.player.shot_type == 'burst':
				self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.burst_ammo)
				self.balloon_ammo_tile.icon = self.burst_shot_icon
			elif self.player.shot_type == 'magic':
				self.balloon_ammo_tile.icon = self.magic_shot_icon
				self.balloon_ammo_tile.update(tile_x, self.screen.get_height(), self.player.magic_ammo)
		elif self.state == 'mainmenu':
			title_x, title_y = toolbox.centeringCoords(self.title_image, self.screen)
			self.screen.blit(self.title_image, (title_x, title_y - 40))
			text_x, text_y = toolbox.centeringCoords(self.start_text, self.screen)
			self.screen.blit(self.start_text, (text_x, text_y + 100))
			text_x, text_y = toolbox.centeringCoords(self.tutorial_text, self.screen)
			text_y = self.screen.get_height() - 30
			self.screen.blit(self.tutorial_text, (text_x, text_y))
		elif self.state == 'gameover':
			text_x, text_y = toolbox.centeringCoords(self.game_over_text, self.screen)
			self.screen.blit(self.game_over_text, (text_x, text_y - 40))
			self.score_text = self.hud_font.render("Final Score: " + str(self.player.score) , True, (255, 12, 13))
			text_x, text_y = toolbox.centeringCoords(self.score_text, self.screen)
			self.screen.blit(self.score_text, (text_x, text_y))
			button_x, button_y = toolbox.centeringCoords(self.reset_button, self.screen)
			button_rect = self.screen.blit(self.reset_button, (button_x, button_y + 80))
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_position = pygame.mouse.get_pos()
					if button_rect.collidepoint(mouse_position):
						self.state = 'mainmenu'

class AmmoTile():
	def __init__(self, screen, icon, font):
		self.screen = screen
		self.icon = icon
		self.font = font
		self.bg_image = pygame.image.load('../assets/hudTile.png')
		self.width = self.bg_image.get_width()

	def update(self, x, y, ammo):
		# Draw tile background
		tile_rect = self.bg_image.get_rect()
		tile_rect.bottomleft = (x, y)
		self.screen.blit(self.bg_image, tile_rect)
		# Draw icon
		icon_rect = self.icon.get_rect()
		icon_rect.center = tile_rect.center
		self.screen.blit(self.icon, icon_rect)
		# Draw ammon number/ ammount
		ammo_text = self.font.render(str(ammo), True, (255, 255, 255))
		self.screen.blit(ammo_text, tile_rect.topleft)
