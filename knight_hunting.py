import pygame, random, sys

def sub_game(width, height, display, gold):
	pygame.init()
	# Defind SOME color
	PINK = (158, 50, 168)
	GREEN = (30, 189, 38)
	ORANGE = (217, 101, 7)
	BLUE = (10, 43, 173)
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	YELLOW = (209, 206, 23)
	
	
	# Create surface
	global WINDOW_WIDTH, WINDOW_HEIGHT
	WINDOW_WIDTH = width
	WINDOW_HEIGHT = height
	# FPS
	FPS = 60
	clock = pygame.time.Clock()
	
	class Button():
		def __init__(self, x, y, image, scale):
			width = image.get_width()
			height = image.get_height()
			self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
			self.rect = self.image.get_rect()
			self.rect.center = (x, y)
			self.pos_unhover = (x, y)
			self.pos_hover = (x, y - 3)
			self.origin_rect = self.image.get_rect()
			self.origin_rect.center = (x, y)
		
		def draw(self, surface):
			surface.blit(self.image, self.rect)
			pos = pygame.mouse.get_pos()
			if self.origin_rect.collidepoint(pos):
				self.rect.center = self.pos_hover
			else:
				self.rect.center = self.pos_unhover
				
	# Define class
	class Game():
		def __init__(self, player, monster_group):
			self.gold = gold
			self.player = player
			self.monster_group = monster_group
			self.score = 0
			self.round = 1
			self.time = 0
			self.frame_count = 0
			self.target_monster = random.choice(monster_group.sprites())
			self.target_type = self.target_monster.type
			self.display_surface = display
			# font
			self.font = pygame.font.Font("./asset2/font.ttf", 32)
			self.colors = [BLUE, GREEN, PINK, ORANGE]
			
			# Define sound
			self.collect_sound = pygame.mixer.Sound("./asset2/collect.mp3")
			self.backgr_music = pygame.mixer.Sound("./asset2/music.mp3")
			self.miss_sound = pygame.mixer.Sound("./asset2/miss.mp3")
			self.game_over_sound = pygame.mixer.Sound("./asset2/gameover.wav")
		
		def check_collide(self):
			collied_monster = pygame.sprite.spritecollideany(player, monster_group)
			if collied_monster:
				if collied_monster.type == self.target_type:
					self.score += self.round * 100
					collied_monster.remove(monster_group)
					self.collect_sound.play()
					# Check monster group contain monster
					if monster_group:
						self.choose_new_target()
					else:
						self.round += 1
						self.start_new_round()
				# MEET sai con
				else:
					self.player.lives -= 1
					self.player.warps()
					self.miss_sound.play()
					# Check lose
					if self.player.lives <= 0:
						self.game_over_sound.play()
						self.pause_game("You LOSE, Press ENTER to PlayAgain")
						self.reset_game()
		
		def start_new_round(self):
			number_monster = 2 * self.round
			for monster in self.monster_group.sprites():
				monster_group.remove(monster)
			for i in range(1, number_monster + 1):
				monster_group.add(
					Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 100 - 64),
					        random.randint(0, 3)))
			self.choose_new_target()
			self.player.come_back()
			self.player.warp += 1
		
		def choose_new_target(self):
			self.target_monster = random.choice(monster_group.sprites())
			self.target_type = self.target_monster.type
		
		def update(self):
			self.frame_count += 1
			if self.frame_count == FPS:
				self.time += 1
				self.frame_count = 0
		
		def draw(self):
			
			score_text = self.font.render(f'Scores:  {self.score}', True, YELLOW)
			score_text_rect = score_text.get_rect()
			score_text_rect.topleft = (10, 10)
			
			lives_text = self.font.render(f'Lives:  {self.player.lives}', True, YELLOW)
			lives_text_rect = lives_text.get_rect()
			lives_text_rect.topright = (WINDOW_WIDTH - 10, 10)
			
			warps_text = self.font.render(f'Warps:  {self.player.warp}', True, YELLOW)
			warps_text_rect = warps_text.get_rect()
			warps_text_rect.topright = (WINDOW_WIDTH - 10, 40)
			
			self.display_surface.blit(score_text, score_text_rect)
			self.display_surface.blit(lives_text, lives_text_rect)
			self.display_surface.blit(warps_text, warps_text_rect)
			
			# Draw target monster
			self.display_surface.blit(self.target_monster.image, (WINDOW_WIDTH // 2, 10, 64, 64))
			
			# Draw the rect restric
			pygame.draw.rect(self.display_surface, self.colors[self.target_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 3)
		
		def pause_game(self, text):
			font = pygame.font.Font("./asset2/font.ttf", 46)
			
			#point text
			bet_text = font.render(f'+ {self.score // 5}', True, GREEN)
			self.gold += self.score // 5

			bet_text_rect = bet_text.get_rect()
			bet_text_rect.topleft = ( int(WINDOW_WIDTH * 0.03)
			                         , int(WINDOW_HEIGHT * 0.75) + gold_text_rect.height)

			#Gold text
			gold_text = font.render(f'GOLD: {self.gold}', True, YELLOW)
			gold_text_rect = gold_text.get_rect()
			gold_text_rect.topleft = (int(WINDOW_WIDTH * 0.03), int(WINDOW_HEIGHT * 0.75))
			
			#Back btn
			image = pygame.image.load("./asset/button/button_back.png")
			scale = image.get_height() / image.get_width()
			
			image = pygame.transform.scale(image, (int(0.15 * WINDOW_WIDTH)
			                                       , int(scale * 0.15 * WINDOW_WIDTH)))
			
			back_button = Button(int((1 - 0.03 - 0.075) * WINDOW_WIDTH)
			                     , int(0.88 * WINDOW_HEIGHT), image, 1)
			
			pause = True
			
			self.backgr_music.stop()
			
			pause_text = font.render(text, True, YELLOW)
			pause_text_rect = pause_text.get_rect()
			pause_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
			while pause:

				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							pause = False
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						if back_button.rect.collidepoint(pos):
							self.backgr_music.stop()
							global running
							running = False
							return
					
				#refresh
				self.display_surface.fill(BLACK)
				#gold text , score text , pause text
				self.display_surface.blit(pause_text, pause_text_rect)
				self.display_surface.blit(gold_text, gold_text_rect)
				self.display_surface.blit(bet_text, bet_text_rect)
				back_button.draw(self.display_surface)
				clock.tick(60)
				
			self.backgr_music.play(-1)
		
		def pause_start_game(self, text):
			font = pygame.font.Font("./asset2/font.ttf", 46)
			
			
			pause = True
			
			self.backgr_music.stop()
			
			pause_text = font.render(text, True, YELLOW)
			pause_text_rect = pause_text.get_rect()
			pause_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
			while pause:
				
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							pause = False
				
				# refresh
				self.display_surface.fill(BLACK)
				# gold text , score text , pause text
				self.display_surface.blit(pause_text, pause_text_rect)
				clock.tick(60)
			
			self.backgr_music.play(-1)
			
		def reset_game(self):
			self.player.reset()
			self.score = 0
			self.round = 1
			self.start_new_round()
	
	
	class Player(pygame.sprite.Sprite):
		def __init__(self):
			super().__init__()
			self.image = pygame.image.load("./asset2/knight.png")
			self.rect = self.image.get_rect()
			self.rect.centerx = WINDOW_WIDTH // 2
			self.rect.bottom = WINDOW_HEIGHT
			self.lives = 4
			self.speed = 8
			self.warp = 2
			self.warp_sound = pygame.mixer.Sound("./asset2/warp_sound.mp3")
		
		def update(self):
			keys = pygame.key.get_pressed()
			if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
				self.rect.x -= self.speed
			if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WINDOW_WIDTH:
				self.rect.x += self.speed
			if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.top > 100:
				self.rect.y -= self.speed
			if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < WINDOW_HEIGHT:
				self.rect.y += self.speed
		
		def warps(self):
			self.warp -= 1
			self.warp_sound.play()
			self.rect.centerx = WINDOW_WIDTH // 2
			self.rect.bottom = WINDOW_HEIGHT
		
		def come_back(self):
			self.rect.centerx = WINDOW_WIDTH // 2
			self.rect.bottom = WINDOW_HEIGHT
		
		def reset(self):
			self.rect.centerx = WINDOW_WIDTH // 2
			self.rect.bottom = WINDOW_HEIGHT
			self.lives = 4
			self.warp = 2
	
	
	class Monster(pygame.sprite.Sprite):
		def __init__(self, x, y, type):
			super().__init__()
			self.type = type
			blue_monster = pygame.image.load("./asset2/blue_monster.png")
			green_monster = pygame.image.load("./asset2/green_monster.png")
			pink_monster = pygame.image.load("./asset2/pink_monster.png")
			orange_monster = pygame.image.load("./asset2/orange_monster.png")
			self.images = [blue_monster, green_monster, pink_monster, orange_monster]
			self.image = self.images[self.type]
			self.rect = self.image.get_rect()
			self.rect.topleft = (x, y)
			self.speed = random.randint(1,3)
			self.dx = random.choice([-1, 1])
			self.dy = random.choice([-1, 1])
		
		def update(self):
			self.rect.x += self.dx * self.speed
			self.rect.y += self.dy * self.speed
			if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
				self.dx *= -1
			if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 100:
				self.dy *= -1
	
	# SPRITE GRP
	player_group = pygame.sprite.Group()
	player = Player()
	player_group.add(player)
	
	monster_group = pygame.sprite.Group()
	monster_group.add(
		Monster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 100 - 64), random.randint(0, 3)))
	
	
	sub_game = Game(player, monster_group)
	sub_game.pause_start_game("Tap enter to play!")
	sub_game.backgr_music.play(-1)
	sub_game.start_new_round()
	
	# MAIN GAME LOOP
	global running
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and sub_game.player.warp > 0 and sub_game.player.rect.bottom <= WINDOW_HEIGHT - 100:
					sub_game.player.warps()
		
		# Fill the back
		sub_game.display_surface.fill((0, 0, 0))
		
		# Check Collied
		sub_game.check_collide()
		
		# BLIT ASSET
		sub_game.update()
		sub_game.draw()
		
		player_group.update()
		player_group.draw(sub_game.display_surface)
		
		monster_group.update()
		monster_group.draw(sub_game.display_surface)
		# Update display and clock
		pygame.display.update()
		clock.tick(FPS)
	
	
	return sub_game.gold


#sub_game(1200,675,pygame.display.set_mode((1200,675)),100)