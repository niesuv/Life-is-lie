import pygame, random, sys

# FPS and clock
FPS = 60
clock = pygame.time.Clock()
# Define Colors
GREEN = (10, 50, 10)
BLACK = (0, 0, 0)

# Create Display Surface(SCALE = 16 / 9)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.x = x
		self.y = y
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.pos_unhover = (x, y)
		self.pos_hover = (x, y - 2)
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			self.rect.center = self.pos_hover
		else:
			self.rect.center = self.pos_unhover


class Game():
	def __init__(self):
		self.scroll = 0
		self.direction_scroll = 1
		# Get BACKGROUND
		image = pygame.image.load("./asset/image/back.webp").convert()
		scale = int(image.get_width() / image.get_height())
		self.back_ground_image = pygame.transform.scale(image, (int(WINDOW_HEIGHT * scale), WINDOW_HEIGHT))
		
		#Font
		self.font32 = pygame.font.Font("./asset/font/font1.ttf",32)
		
		# Game Value, SET in TEXT file
		self.gold = 1000
		self.map = 1
		self.set = 1
		self.bet = 1
		self.history = []
	
	def main(self):
		running = True
		while running:
			# Check close
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				self.show_main_menu()
			clock.tick(FPS)
	
	def show_main_menu(self):
		# Music
		self.menu_music = pygame.mixer.Sound("./asset/music/menu_music.mp3")
		# Button menu
		start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
		                      pygame.image.load("./asset/button/start_button.png"), 0.2)
		setting_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 130,
		                        pygame.image.load("./asset/button/setting_button.png"), 0.2)
		
		main_menu_run = True
		self.menu_music.play(-1)
		
		while main_menu_run:
			self.show_back_ground()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				# CHECK CLICK BUTTON
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					if start_button.rect.collidepoint(pos):
						self.start_new_round()
					
					if setting_button.rect.collidepoint(pos):
						self.show_setting()
			
			start_button.draw(display_surface)
			setting_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_back_ground(self):
		if self.scroll <= 0:
			self.direction_scroll = 1
		if self.scroll >= self.back_ground_image.get_width() - WINDOW_WIDTH:
			self.direction_scroll = -1
		self.scroll += self.direction_scroll * .5
		display_surface.blit(self.back_ground_image, (-self.scroll, 0))
	
	def start_new_round(self):
		self.show_map()
		self.show_set()
		self.show_bet()
		self.race()
	
	def show_setting(self):
		pass
	
	def show_bet(self):
		pass
	
	def show_map(self):
		# SET BUTTON
		image = pygame.image.load("./asset/map/map1.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (300 * scale, 300))
		map_button1 = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, image, 1)
		
		mapping = True
		while mapping:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					if map_button1.rect.collidepoint(pos):
						self.map = 1
						mapping = False
			display_surface.fill(BLACK)
			map_button1.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_set(self):
		pass
	
	def show_victory(self):
		pass
	
	def show_HUD(self):
		pass
	
	def race(self):
		self.menu_music.stop()
		racing = True
		map = pygame.transform.scale(pygame.image.load(f"./asset/map/map{self.map}.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
		backmap = pygame.image.load(f"./asset/map/backmap{self.map}.jpg")
		scale = backmap.get_width() / backmap.get_height()
		backmap = pygame.transform.scale(backmap,(WINDOW_HEIGHT * scale,WINDOW_HEIGHT))
		player_group = pygame.sprite.Group()
		for i in range(1, 6):
			player = Player(i, 0, WINDOW_HEIGHT * 0.263351 + (i - 1) * WINDOW_HEIGHT * 0.17407407407)
			player_group.add(player)
		scroll = 0
		while racing:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					
			#Scroll the back_ground behide
			scroll += 1
			if scroll >= backmap.get_width():
				scroll = 0
			for i in range(3):
				display_surface.blit(backmap,(i * backmap.get_width() - scroll, 0))
				
			#Blit the road
			display_surface.blit(map, (0, 0))
			
		
			#Run the player
			player_group.update()
			player_group.draw(display_surface)
			
			#Blit the HUD
			self.show_HUD()
			
			pygame.display.update()
			clock.tick(FPS)


class Player(pygame.sprite.Sprite):
	def __init__(self, index, x, y):
		super().__init__()
		self.index = index
		self.speed = random.uniform(1,2)
		self.animate_fps = .3
		self.frame = []
		for i in range(9):
			image = pygame.image.load(f"./asset/set/1/{i + 1}.png")
			scale = image.get_width() / image.get_height()
			self.frame.append(pygame.transform.scale(image, (WINDOW_HEIGHT*0.15*scale, WINDOW_HEIGHT*0.15)))
		
		self.current_frame = 0
		self.image = self.frame[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (x, y)
		self.positonx = x
	
	def update(self):
		if self.rect.right <= WINDOW_WIDTH:
			self.positonx += self.speed
			self.rect.x = int(self.positonx)
			self.animate(self.animate_fps)
	
	def animate(self, fps):
		self.current_frame += fps
		if self.current_frame >= 8:
			self.current_frame = 0
		self.image = self.frame[int(self.current_frame)]


pygame.init()
my_game = Game()
my_game.main()
