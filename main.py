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
		self.pos_hover = (x, y - 3)
		
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
		
		
		self.menu_music.stop()
		self.menu_music.play(-1)
		
		main_menu_run = True
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
	
	def show_setting(self):
		#Set button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale), int(0.0688 * WINDOW_HEIGHT)))
		# GO BACK BUTTON
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
		setting = True
		while setting:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# Check click Map
					if go_back_button.rect.collidepoint(pos):
						setting = False
			
			self.show_back_ground()
			# DRAW BUTTON
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_bet(self):
		
		#Load thumbnail
		
		
		#Go back button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale), int(0.0688 * WINDOW_HEIGHT)))
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
		betting  = True
		while betting:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# Check click GO BaCK
					if go_back_button.rect.collidepoint(pos):
						betting = False
					
			self.show_back_ground()
			# DRAW BUTTON
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_map(self):
		# SET BUTTON
		image = pygame.image.load(f"./asset/map/showmap1.png")
		image = pygame.transform.scale(image, (int(0.271 * WINDOW_WIDTH),int(0.271 * WINDOW_HEIGHT)))
		images = [image,image,image,image,image,image]
		self.map_thumbnail = []
		#Chua te hard code
		for i in range(6):
			if i <= 2:
				self.map_thumbnail.append(Button(int(i*(images[i].get_width() + 0.040 * WINDOW_WIDTH )
				                          + 0.051 * WINDOW_WIDTH + images[i].get_width() / 2)  ,int(0.314 * WINDOW_HEIGHT)
				                      ,images[i],1))
			else:
				self.map_thumbnail.append(Button(int((i-3)*(images[i].get_width() + 0.040 * WINDOW_WIDTH )
				                          + 0.051 * WINDOW_WIDTH + images[i].get_width() / 2),
				                      int((0.314 +0.377) * WINDOW_HEIGHT ),images[i],1 ))
		# GO BACK BUTTON
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale),int(0.0688 * WINDOW_HEIGHT)))
		go_back_button = Button(int(0.051*WINDOW_WIDTH + image.get_width() / 2), int(0.075*WINDOW_HEIGHT),image, 1)
		mapping = True
		while mapping:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					#Check click Map
					for i in range(6):
						if self.map_thumbnail[i].rect.collidepoint(pos):
							self.map = 1
							self.show_set()
					if go_back_button.rect.collidepoint(pos):
						mapping = False
						
			self.show_back_ground()
			#DRAW BUTTON
			for i in range(6):
				self.map_thumbnail[i].draw(display_surface)
				
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_set(self):
		#Lay ra anh thumbnail
		image = pygame.image.load(f"./asset/set/set1/set_avt/all_set1.png")
		image = pygame.transform.scale(image, (int(0.286 * WINDOW_HEIGHT), int(0.286 * WINDOW_HEIGHT)))
		images = [image, image, image, image, image, image]
		self.sets_thumbnail = []
		# Chua te hard code
		for i in range(5):
			if i <= 2:
				self.sets_thumbnail.append(Button(int(0.192 * WINDOW_WIDTH + i * (0.16 + 0.146)*WINDOW_WIDTH)
				                        ,int(0.317 * WINDOW_HEIGHT),images[i],1))
			else:
				self.sets_thumbnail.append(Button(int(0.192 * WINDOW_WIDTH + (i-3) * (0.16 + 0.146) * WINDOW_WIDTH)
				                       , int(0.7196 * WINDOW_HEIGHT), images[i], 1))
		# Set button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale), int(0.0688 * WINDOW_HEIGHT)))
		# GO BACK BUTTON
		
		
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
		chosing_set = True
		while chosing_set:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					# Check click GO BaCK
					if go_back_button.rect.collidepoint(pos):
						chosing_set = False
					#Check chosing set
					for i in range(5):
						if self.sets_thumbnail[i].rect.collidepoint(pos):
							self.set = 1
							self.show_bet()
			self.show_back_ground()
			# DRAW BUTTON
			for i in range(5):
				self.sets_thumbnail[i].draw(display_surface)
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
		
	
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
			image = pygame.image.load(f"./asset/set/set{my_game.set}/{self.index}/{i + 1}.png")
			scale = image.get_width() / image.get_height()
			self.frame.append(pygame.transform.scale(image, (int(WINDOW_HEIGHT*0.15*scale), int(WINDOW_HEIGHT*0.15))))
		
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
