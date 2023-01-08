import sys
import pygame, random

def sub_game(width, height, gold, music):
	GREEN = (30, 189, 38)
	ORANGE = (217, 101, 7)
	YELLOW = (209, 206, 23)
	
	
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
				
	global return_gold
	return_gold = gold
	pygame.init()
	
	# Set display sureface
	WINDOW_WIDTH = width
	WINDOW_HEIGHT = height
	display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	
	# FPS AND Clock
	clock = pygame.time.Clock()
	FPS = 60
	
	# Define Colors
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	GREEN = (0, 255, 0)
	DARK_GREEN = (10, 50, 10)
	ORANGE = (238, 141, 70)
	
	# Game Value
	if WINDOW_WIDTH == 1200:
		BURGER_BEGIN_SPEED = 7
	else:
		BURGER_BEGIN_SPEED = 8
	
	ACCELERATION = .1
	DOG_DEFAULT_SPEED = 8
	DOG_BOOST_SPEED = 20
	DOG_BEGIN_BOOST_LEVEL = 100
	DOG_LIVES = 2
	boost_level = DOG_BEGIN_BOOST_LEVEL
	point = 0
	lives = DOG_LIVES
	dog_speed = DOG_DEFAULT_SPEED
	
	# Load Music
	bark_sound = pygame.mixer.Sound("./asset3/bark_sound.wav")
	miss_sound = pygame.mixer.Sound("./asset3/miss.mp3")
	boost_sound = pygame.mixer.Sound("./asset3/boost_sound.wav")
	game_over_sound = pygame.mixer.Sound("./asset3/gameover.wav")
	pygame.mixer.music.load("./asset3/music.mp3")
	pygame.mixer.music.set_volume(.4)
	
	# Load DOG
	bg = pygame.image.load("./asset3/bg.png")
	right_dog = pygame.image.load("./asset3/right_dog.png")
	left_dog = pygame.image.load("./asset3/left_dog.png")
	dog = right_dog
	dog_rect = dog.get_rect()
	dog_rect.centerx = WINDOW_WIDTH / 2
	dog_rect.bottom = WINDOW_HEIGHT
	meat = pygame.image.load("./asset3/meat.png")
	meat_rect = meat.get_rect()
	
	# Load Text
	font = pygame.font.Font('./asset3/font.ttf', 32)
	font2 = pygame.font.Font('./asset3/font.ttf', 46)
	
	point_text = font.render(f'Point:  {point}', True, GREEN)
	point_text_rect = point_text.get_rect()
	point_text_rect.topleft = (32, 32)
	
	live_text = font.render(f'Lives:  {lives}', True, GREEN)
	live_text_rect = live_text.get_rect()
	live_text_rect.topright = (WINDOW_WIDTH - 32, 32)
	
	game_over_text = font2.render("GAME OVER, PRESS ENTER TO CONTINUE!", True, ORANGE)
	game_over_text_rect = game_over_text.get_rect()
	game_over_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
	
	boost_text = font.render(f'BOOST ENERGY:  {boost_level}', True, ORANGE)
	boost_text_rect = boost_text.get_rect()
	boost_text_rect.centerx = WINDOW_WIDTH // 2
	boost_text_rect.y = 32
	
	# BEGIN GAME
	if music:
		pygame.mixer.music.play(-1)
	boost_level = DOG_BEGIN_BOOST_LEVEL
	point = 0
	lives = DOG_LIVES
	dog_speed = DOG_DEFAULT_SPEED
	dog_rect.centerx = WINDOW_WIDTH / 2
	dog_rect.bottom = WINDOW_HEIGHT
	meat_rect.bottomleft = (random.randint(0, WINDOW_WIDTH - 72), 100)
	burger_speed = BURGER_BEGIN_SPEED
	
	backgr = pygame.image.load("./asset/image/cheems_back.png")
	backgr = pygame.transform.scale(backgr, (WINDOW_WIDTH, WINDOW_HEIGHT));
	
	# MAIN GAME LOOP
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		# Control the Dog
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and dog_rect.left > 0:
			dog_rect.x -= dog_speed
			dog = left_dog
		
		if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and dog_rect.right < WINDOW_WIDTH:
			dog_rect.x += dog_speed
			dog = right_dog
		
		if (keys[pygame.K_UP] or keys[pygame.K_w]) and dog_rect.top > 100:
			dog_rect.y -= dog_speed
		
		if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and dog_rect.bottom < WINDOW_HEIGHT:
			dog_rect.y += dog_speed
		
		if keys[pygame.K_SPACE] and boost_level > 0:
			boost_level -= 1
			if dog_speed != DOG_BOOST_SPEED:
				if music:
					boost_sound.play()
			dog_speed = DOG_BOOST_SPEED
		
		else:
			dog_speed = DOG_DEFAULT_SPEED
			boost_sound.stop()
		
		# Move the Meat
		meat_rect.y += burger_speed
		
		# Check Meat
		if meat_rect.colliderect(dog_rect):
			point += 10
			burger_speed += ACCELERATION
			boost_level += 50
			meat_rect.bottomleft = (random.randint(0, WINDOW_WIDTH - 72), 100)
			if music:
				bark_sound.play()
		if meat_rect.y > WINDOW_HEIGHT:
			if music:
				miss_sound.play()
			lives -= 1
			meat_rect.bottomleft = (random.randint(0, WINDOW_WIDTH - 72), 100)
		
		# Refresh the SCREEN
		display_surface.blit(backgr, (0, 0))
		
		# Load Text ReRender
		point_text = font.render(f'Point:  {point}', True, GREEN)
		boost_text = font.render(f'BOOST ENERGY:  {boost_level}', True, ORANGE)
		live_text = font.render(f'Lives:  {lives}', True, GREEN)
		display_surface.blit(bg, (0,0))
		display_surface.blit(boost_text, boost_text_rect)
		display_surface.blit(point_text, point_text_rect)
		display_surface.blit(live_text, live_text_rect)
		pygame.draw.line(display_surface, DARK_GREEN, (0, 97), (WINDOW_WIDTH, 97), 3)
		
		# Check lose
		if lives == 0:
			pause = True
			# Gold text
			gold_text = font.render(f'GOLD: {return_gold + point}', True, YELLOW)
			gold_text_rect = gold_text.get_rect()
			gold_text_rect.topleft = (int(WINDOW_WIDTH * 0.03), int(WINDOW_HEIGHT * 0.75))
			
			# point text
			bet_text = font.render(f'+ {point}', True, GREEN)
			return_gold += point
			
			bet_text_rect = bet_text.get_rect()
			bet_text_rect.topleft = (int(WINDOW_WIDTH * 0.03), int(WINDOW_HEIGHT * 0.75) + gold_text_rect.height)
			
			# Back button
			image = pygame.image.load("./asset/button/button_back.png")
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.15 * WINDOW_WIDTH), int(scale * 0.15 * WINDOW_WIDTH)))
			back_button = Button(int((1 - 0.03 - 0.075) * WINDOW_WIDTH), int(0.88 * WINDOW_HEIGHT), image, 1)

			if music:
				game_over_sound.play()
			
			while pause:
				display_surface.blit(game_over_text, game_over_text_rect)
				display_surface.blit(gold_text, gold_text_rect)
				display_surface.blit(bet_text, bet_text_rect)
				back_button.draw(display_surface)
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_RETURN:
							pause = False
							game_over_sound.stop()
							if music:
								pygame.mixer.music.play(-1)
							boost_level = DOG_BEGIN_BOOST_LEVEL
							point = 0
							lives = DOG_LIVES
							dog_speed = DOG_DEFAULT_SPEED
							dog_rect.centerx = WINDOW_WIDTH / 2
							dog_rect.bottom = WINDOW_HEIGHT
							meat_rect.bottomleft = (random.randint(0, WINDOW_WIDTH - 72), 100)
							burger_speed = BURGER_BEGIN_SPEED
					
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						if back_button.rect.collidepoint(pos):
							game_over_sound.stop()
							boost_sound.stop()
							pygame.mixer.music.stop()
							return return_gold
		
		# Load the dog
		display_surface.blit(dog, dog_rect)
		display_surface.blit(meat, meat_rect)
		
		# UPDATE DISPLAY AND SET CLOCK
		pygame.display.update()
		clock.tick(FPS)